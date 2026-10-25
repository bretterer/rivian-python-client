"""Tests for signed Parallax commands and the state messages that report on them."""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import uuid
from typing import Any
from unittest.mock import patch

import pytest

from rivian.parallax import (
    decode_command_state_message,
    encode_command,
    encode_lock,
    encode_unlock,
)
from rivian.parallax.command import decode_command_state
from rivian.parallax.proto import command_pb2 as command
from rivian.utils import generate_key_pair, get_secret_key

RVM = "body.locks.unlock"
COMMAND_ID = uuid.UUID(bytes=bytes(range(16)))
NOW_MS = 1_700_000_000_123
# The signature the vehicle accepted on GOLDEN, injected so the test needs no keys
SIGNATURE = bytes.fromhex(
    "41b86b3b3f6c5b96d09abf3f77e87af7bbdbc7ef40bed7861b112b154e5c2dd0"
)
# An unlock as app 3.17.0 sends it, captured from a request an R1T carried out in
# 2026-10 and then sanitized: the ids are made up and the signature is injected.
# It proves the framing; test_encode_command proves the signature.
GOLDEN = (
    "524512430a11626f64792e6c6f636b732e756e6c6f636b10031a10000102030405060708090a0b0c"
    "0d0e0f220208012a0b0880e2cfaa0610c0a9d33a3a0976656869636c652d31620b0880e2cfaa0610"
    "c0a9d33a820110000102030405060708090a0b0c0d0e0f8a01320a240801122041b86b3b3f6c5b96"
    "d09abf3f77e87af7bbdbc7ef40bed7861b112b154e5c2dd0120a6964656e746974792d31"
)


def _keys() -> dict[str, str]:
    """The arguments of encode_command that are a phone's and a vehicle's keys."""
    vehicle_key, _ = generate_key_pair()
    _, private_key = generate_key_pair()
    return {
        "identity_id": "identity-1",
        "vehicle_key": vehicle_key,
        "private_key": private_key,
    }


def _envelope(encoded: str) -> command.Envelope:
    return command.Envelope.FromString(base64.b64decode(encoded))


def _operation(envelope: command.Envelope) -> command.Operation:
    return command.Operation.FromString(envelope.composite.bytes_val)


def test_encode_command_matches_a_payload_a_vehicle_accepted() -> None:
    """The encoding is byte for byte what was sent to a real vehicle."""
    with patch(
        "rivian.parallax.command.generate_ble_command_hmac", return_value=SIGNATURE
    ):
        encoded = encode_command(
            "vehicle-1",
            RVM,
            encode_unlock(),
            identity_id="identity-1",
            vehicle_key="vehicle_key",
            private_key="private_key",
            command_id=str(COMMAND_ID),
            timestamp=NOW_MS,
        )
    assert base64.b64decode(encoded).hex() == GOLDEN


def test_encode_command() -> None:
    """The operation is signed with the secret both keys derive."""
    phone_public, phone_private = generate_key_pair()
    vehicle_public, vehicle_private = generate_key_pair()

    envelope = _envelope(
        encode_command(
            "vehicle-1",
            RVM,
            encode_unlock(),
            identity_id="identity-1",
            vehicle_key=vehicle_public,
            private_key=phone_private,
            command_id=str(COMMAND_ID),
            timestamp=NOW_MS,
        )
    )
    operation = _operation(envelope)
    assert operation.rvm == RVM
    assert operation.type == command.PARALLAX_OPERATION_REQUEST
    assert operation.command_id == COMMAND_ID.bytes == envelope.correlation_id
    assert operation.payload == encode_unlock()
    assert operation.vehicle_id == "vehicle-1"
    for stamp in (operation.created_at, envelope.last_update):
        assert (stamp.seconds, stamp.nanos) == (1_700_000_000, 123_000_000)

    # The vehicle derives the same secret from its own key and the phone's
    secret = get_secret_key(vehicle_private, phone_public)
    signature = envelope.security_info.signature
    assert signature.type == command.DATA_SIGNATURE_TYPE_HMAC_SHA256
    assert (
        signature.value
        == hmac.new(secret, envelope.composite.bytes_val, hashlib.sha256).digest()
    )
    assert envelope.security_info.mapped_identity == "identity-1"


def test_encode_command_defaults() -> None:
    """Each command gets a new id and the time now, unless given; a lock has no payload."""
    args = ("vehicle-1", "body.locks.lock", encode_lock())
    with patch("rivian.parallax.command.time.time", return_value=1_700_000_000.5):
        first = _envelope(encode_command(*args, **_keys()))
        second = _envelope(encode_command(*args, **_keys()))
    assert len(first.correlation_id) == 16
    assert first.correlation_id != second.correlation_id
    assert uuid.UUID(bytes=first.correlation_id).version == 4
    assert (first.last_update.seconds, first.last_update.nanos) == (
        1_700_000_000,
        500_000_000,
    )
    assert _operation(first).payload == b""


@pytest.mark.parametrize(
    ("timestamp", "seconds", "nanos"),
    [
        (1_700_000_000_999, 1_700_000_000, 999_000_000),  # cut, not rounded
        (0, 0, 0),  # a time, not 'now'
    ],
)
def test_encode_command_timestamp(timestamp: int, seconds: int, nanos: int) -> None:
    """The timestamp is epoch milliseconds."""
    stamp = _envelope(
        encode_command("vehicle-1", RVM, b"", **_keys(), timestamp=timestamp)
    ).last_update
    assert (stamp.seconds, stamp.nanos) == (seconds, nanos)


@pytest.mark.parametrize("command_id", ["not-a-uuid", ""])
def test_encode_command_with_an_invalid_command_id(command_id: str) -> None:
    """The id must be a UUID, even an empty one."""
    with pytest.raises(ValueError):
        encode_command("vehicle-1", RVM, b"", **_keys(), command_id=command_id)


def _state(
    progress: int = command.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_COMPLETE,
    command_id: bytes = COMMAND_ID.bytes,
    **result: Any,
) -> str:
    """The payload of a `vehicleCommandStatePx` message."""
    message = command.CommandState(
        command_id=command_id, rvm=RVM, progress=progress, **result
    )
    return base64.b64encode(message.SerializeToString()).decode()


def _complete(**result: Any) -> str:
    return _state(data=command.CommandResult(**result))


@pytest.mark.parametrize(
    ("progress", "expected"),
    [
        (command.VEHICLE_MODEL_OP_PROGRESS_UNSPECIFIED, "unspecified"),
        (command.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_WAKING_UP, "waking_up"),
        (command.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_VALIDATING, "validating"),
        (command.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_EXECUTING, "executing"),
        (command.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_COMPLETE, "complete"),
    ],
)
def test_decode_progress(progress: int, expected: str) -> None:
    """Before the result there is a progress and no status."""
    assert decode_command_state(_state(progress)) == {
        "commandId": str(COMMAND_ID),
        "rvm": RVM,
        "progress": expected,
        "status": None,
        "error": None,
    }


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (command.RESPONSE_STATUS_UNDEFINED, "undefined"),
        (command.RESPONSE_STATUS_SUCCESS, "success"),
        (command.RESPONSE_STATUS_FAIL, "failed"),
        (command.RESPONSE_STATUS_INVALID_REQUEST, "invalid_request"),
        (command.RESPONSE_STATUS_NOT_SUPPORTED, "not_supported"),
        (command.RESPONSE_STATUS_TIMEOUT, "timeout"),
    ],
)
def test_decode_status(status: int, expected: str) -> None:
    """A result has a status, even the default one that protobuf leaves out."""
    result = decode_command_state(_complete(response_status=status))
    assert result is not None
    assert result["progress"] == "complete"
    assert result["status"] == expected
    assert result["error"] is None


def test_decode_result_error() -> None:
    """The result's own error is kept, with the status."""
    result = decode_command_state(
        _complete(
            response_status=command.RESPONSE_STATUS_FAIL,
            error=command.Error(code=22, message="not now"),
        )
    )
    assert result is not None
    assert result["status"] == "failed"
    assert result["error"] == {"code": 22, "message": "not now"}


def test_decode_operation_error() -> None:
    """If the whole operation failed there is an error and no status."""
    result = decode_command_state(
        _state(operation_error=command.OperationError(error=7, message="bad"))
    )
    assert result is not None
    assert result["status"] is None
    assert result["error"] == {"code": 7, "message": "bad"}


def test_decode_unknown_values(caplog: pytest.LogCaptureFixture) -> None:
    """Values the schema doesn't know are kept as numbers, and logged."""
    caplog.set_level(logging.DEBUG, logger="rivian.parallax.core")
    result = decode_command_state(
        _state(
            progress=9,
            command_id=b"short",
            data=command.CommandResult(response_status=9),
        )
    )
    assert result is not None
    assert result["progress"] == 9
    assert result["status"] == 9
    assert result["commandId"] is None
    assert "Unknown command progress value: 9" in caplog.text
    assert "Unknown command status value: 9" in caplog.text


def test_decode_logs_the_message(caplog: pytest.LogCaptureFixture) -> None:
    """What was received is debug-logged, like for the other Parallax messages."""
    caplog.set_level(logging.DEBUG, logger="rivian.parallax.core")
    decode_command_state(_state())
    assert "command state: " in caplog.text
    assert "progress: VEHICLE_MODEL_OP_PROGRESS_VEHICLE_COMPLETE" in caplog.text


@pytest.mark.parametrize(
    "payload", ["AAAA", base64.b64encode(b"\xff").decode(), "A", "", "!!!!", None]
)
def test_decode_unreadable(payload: str | None) -> None:
    """A payload that is empty or isn't a state message gives nothing."""
    assert decode_command_state(payload) is None  # type: ignore[arg-type]


def test_decode_state_message() -> None:
    """The state is unwrapped from the whole websocket message."""
    message = {
        "type": "next",
        "id": "subscription-id",
        "payload": {
            "data": {
                "vehicleCommandStatePx": {
                    "payload": _complete(
                        response_status=command.RESPONSE_STATUS_SUCCESS
                    )
                }
            }
        },
    }
    result = decode_command_state_message(message)
    assert result is not None
    assert result["progress"] == "complete"
    assert result["status"] == "success"


@pytest.mark.parametrize(
    "message",
    [
        {"payload": {"errors": [{"message": "no access"}]}},  # an error frame
        {"payload": {"data": {"vehicleCommandStatePx": {"payload": None}}}},
        {"payload": {"data": {"vehicleCommandStatePx": {"payload": 5}}}},
        {"payload": {"data": [1]}},
        {"payload": {"data": {"vehicleCommandStatePx": "text"}}},
        None,
    ],
)
def test_decode_state_message_without_a_state(message: Any) -> None:
    """Error frames and the like give nothing."""
    assert decode_command_state_message(message) is None
