"""Encoder and decoder for signed Parallax remote commands.

A command such as `body.locks.unlock` is sent with the `sendParallaxPayload`
mutation (`Rivian.send_parallax_command`). Its payload is an `Operation` in an
`Envelope`, signed with the secret that `Rivian.send_vehicle_command` derives from
the phone's key and the vehicle's, but over the operation's bytes. In testing,
Rivian woke a sleeping vehicle for it.

The `vehicleCommandStatePx` subscription
(`Rivian.subscribe_for_parallax_command_state`) reports on the command as it
goes: the vehicle waking up, validating and executing it, then the result.
"""

from __future__ import annotations

import base64
import time
import uuid
from typing import Any, Final

from google.protobuf.message import DecodeError

from ..utils import generate_ble_command_hmac
from .core import _LOGGER, _debug_message, _enum, _present
from .proto import command_pb2

_PROGRESS_MAP: Final[dict[int, str]] = {
    command_pb2.VEHICLE_MODEL_OP_PROGRESS_UNSPECIFIED: "unspecified",
    command_pb2.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_WAKING_UP: "waking_up",
    command_pb2.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_VALIDATING: "validating",
    command_pb2.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_EXECUTING: "executing",
    command_pb2.VEHICLE_MODEL_OP_PROGRESS_VEHICLE_COMPLETE: "complete",
}

_STATUS_MAP: Final[dict[int, str]] = {
    command_pb2.RESPONSE_STATUS_UNDEFINED: "undefined",
    command_pb2.RESPONSE_STATUS_SUCCESS: "success",
    command_pb2.RESPONSE_STATUS_FAIL: "failed",
    command_pb2.RESPONSE_STATUS_INVALID_REQUEST: "invalid_request",
    command_pb2.RESPONSE_STATUS_NOT_SUPPORTED: "not_supported",
    command_pb2.RESPONSE_STATUS_TIMEOUT: "timeout",
}


def encode_command(
    vehicle_id: str,
    rvm: str,
    payload: bytes,
    *,
    identity_id: str,
    vehicle_key: str,
    private_key: str,
    command_id: str | None = None,
    timestamp: float | None = None,
) -> str:
    """Encode and sign a command, as the payload of `sendParallaxPayload`.

    `payload` is the RVM's message, e.g. `encode_unlock()` for `UNLOCK_RVM`;
    nothing checks that they go together. `identity_id`, `vehicle_key` and
    `private_key` are the ones `send_vehicle_command` takes. The command id, a
    UUID, is a new one unless `command_id` is given (`ValueError` if it isn't
    one); `timestamp` is epoch milliseconds, now unless given.

    The result is signed and can be replayed until the vehicle rejects its
    timestamp, so treat it as a secret.
    """
    command_id_bytes = (
        uuid.uuid4().bytes if command_id is None else uuid.UUID(command_id).bytes
    )
    timestamp_ms = int(time.time() * 1000 if timestamp is None else timestamp)
    stamp = command_pb2.Timestamp(
        seconds=timestamp_ms // 1000, nanos=timestamp_ms % 1000 * 1_000_000
    )
    operation = command_pb2.Operation(
        rvm=rvm,
        type=command_pb2.PARALLAX_OPERATION_REQUEST,
        command_id=command_id_bytes,
        payload=payload,
        created_at=stamp,
        vehicle_id=vehicle_id,
    ).SerializeToString()
    envelope = command_pb2.Envelope(
        composite=command_pb2.Composite(bytes_val=operation),
        last_update=stamp,
        correlation_id=command_id_bytes,
        security_info=command_pb2.SecurityInfo(
            signature=command_pb2.Signature(
                type=command_pb2.DATA_SIGNATURE_TYPE_HMAC_SHA256,
                # The raw HMAC-SHA256 of the data, as BLE commands use too
                value=generate_ble_command_hmac(operation, vehicle_key, private_key),
            ),
            mapped_identity=identity_id,
        ),
    )
    return base64.b64encode(envelope.SerializeToString()).decode("utf-8")


def decode_command_state(payload: str) -> dict[str, Any] | None:
    """Decode the payload of a `vehicleCommandStatePx` message.

    Returns None if the payload is empty or can't be read.

    Fields:
        commandId: str | None — the command's UUID
        rvm: str
        progress: str | int — "unspecified" | "waking_up" | "validating" |
            "executing" | "complete". Any of the ones before "complete" can be
            skipped, and "waking_up" has come more than once for one command.
        status: str | int | None — how the vehicle answered ("undefined" |
            "success" | "failed" | "invalid_request" | "not_supported" |
            "timeout"); None if the message has no result
        error: dict | None — {"code": int, "message": str}, from the result or,
            if the whole operation failed, from the operation error (which has
            no status)

    A value this library doesn't know comes back as the number it was sent as.

    The vehicle has done the command when the progress is "complete", the status
    "success" and there is no error. "failed", "invalid_request" and
    "not_supported" mean it has not. With "timeout" or "undefined", or if no
    "complete" message comes at all, it isn't known, and the vehicle may do it
    later.
    """
    try:
        data = base64.b64decode(payload)
        message = command_pb2.CommandState.FromString(data)
    except (TypeError, ValueError, DecodeError):
        _LOGGER.debug("Failed to decode command state", exc_info=True)
        return None
    if not data:
        return None
    _debug_message("command state", message)

    status: str | int | None = None
    error: dict[str, Any] | None = None
    if (result := _present(message, "data")) is not None:
        status = _enum(_STATUS_MAP, result.response_status, what="command status")
        if (result_error := _present(result, "error")) is not None:
            error = {"code": result_error.code, "message": result_error.message}
    elif (operation_error := _present(message, "operation_error")) is not None:
        error = {"code": operation_error.error, "message": operation_error.message}
    return {
        "commandId": (
            str(uuid.UUID(bytes=message.command_id))
            if len(message.command_id) == 16
            else None
        ),
        "rvm": message.rvm,
        "progress": _enum(_PROGRESS_MAP, message.progress, what="command progress"),
        "status": status,
        "error": error,
    }


def decode_command_state_message(data: dict[str, Any]) -> dict[str, Any] | None:
    """Decode a raw `subscribe_for_parallax_command_state` message.

    Unwraps `payload.data.vehicleCommandStatePx.payload` for
    `decode_command_state`; returns None if it's missing or can't be read. That
    includes a message that carries GraphQL errors (`data["payload"]["errors"]`)
    instead of a state.
    """
    payload: Any = data
    for key in ("payload", "data", "vehicleCommandStatePx", "payload"):
        if not isinstance(payload, dict):
            return None
        payload = payload.get(key)
    return decode_command_state(payload)
