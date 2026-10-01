"""Tests for the Parallax registry, dispatch, helpers and generated code."""

from __future__ import annotations

import base64
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from rivian.parallax import (
    CHARGING_RVMS,
    PARALLAX_RVMS,
    decode_parallax_message,
    decode_parallax_subscription_message,
)
from rivian.parallax.core import RVMDecoder, _enum
from rivian.parallax.proto import charging_pb2 as charging

from .helpers import epoch

PROTO_DIR = Path(__file__).parents[2] / "src" / "rivian" / "parallax" / "proto"


def test_generated_code_is_current(tmp_path: Path) -> None:
    """The committed *_pb2 modules match what the pinned grpcio-tools protoc generates.

    Regenerate from the repository root with:
        uv run python -m grpc_tools.protoc --proto_path=src --python_out=src \\
            --pyi_out=src src/rivian/parallax/proto/*.proto
    Compiling relative to `src` registers each file as
    `rivian/parallax/proto/<name>.proto`, so it can't collide with another
    library's same-named .proto in protobuf's process-wide descriptor pool.
    The pinned protoc emits gencode Home Assistant's protobuf runtime can
    import; a newer protoc may not.
    """
    src = PROTO_DIR.parents[2]
    protos = sorted(PROTO_DIR.glob("*.proto"))
    subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"--proto_path={src}",
            f"--python_out={tmp_path}",
            f"--pyi_out={tmp_path}",
            *map(str, protos),
        ],
        check=True,
    )
    generated_dir = tmp_path / PROTO_DIR.relative_to(src)
    for generated in sorted(generated_dir.iterdir()):
        committed = PROTO_DIR / generated.name
        assert committed.exists(), f"{generated.name} is missing; regenerate it"
        assert committed.read_text() == generated.read_text(), (
            f"{generated.name} is stale; regenerate it"
        )


def test_registered_proto_file_names_are_namespaced() -> None:
    """Every schema registers under rivian/parallax/proto/, not a bare file name."""
    for message in RVMDecoder.messages.values():
        assert message.DESCRIPTOR.file.name.startswith("rivian/parallax/proto/")


def test_enum() -> None:
    """Known values map; unknown pass through or use the given default."""
    mapping = {1: "one"}
    assert _enum(mapping, None, what="x") is None
    assert _enum(mapping, 1, what="x") == "one"
    assert _enum(mapping, 9, what="x") == 9
    assert _enum(mapping, 9, what="x", unmapped_default="dflt") == "dflt"


def test_decode_parallax_message_dispatch() -> None:
    """Known RVMs decode, unknown RVMs return None, and a timestamp is attached."""
    assert decode_parallax_message("unknown.topic.rvm", "") is None

    payload = charging.SocSlider(soc_limit=80).SerializeToString()
    message: dict[str, Any] = {
        "rvm": "charging.session.soc_slider",
        "payload": base64.b64encode(payload).decode(),
        "timestamp": 1790672961913,
        "extra_field": 123,
    }
    result = decode_parallax_message(**message)
    assert result == {"batteryLimit": 80, "timestamp": epoch(1790672961913)}


def test_decode_parallax_subscription_message() -> None:
    """A raw subscription message is unwrapped before decoding."""
    slider = charging.SocSlider(soc_limit=80).SerializeToString()
    data: dict[str, Any] = {
        "id": "1",
        "type": "next",
        "payload": {
            "data": {
                "parallaxMessages": {
                    "__typename": "ParallaxMessageResponse",
                    "payload": base64.b64encode(slider).decode(),
                    "timestamp": 1790672961913,
                    "rvm": "charging.session.soc_slider",
                }
            }
        },
    }
    assert decode_parallax_subscription_message(data) == {
        "batteryLimit": 80,
        "timestamp": epoch(1790672961913),
    }
    assert decode_parallax_subscription_message({"type": "error"}) is None
    assert decode_parallax_subscription_message({"payload": {"data": None}}) is None


def test_missing_and_corrupt_payloads() -> None:
    """A missing or undecodable payload yields an empty result, not an exception."""
    rvm = "energy.high_voltage.battery_state"
    assert decode_parallax_message(rvm, None) == {}  # type: ignore[arg-type]
    assert decode_parallax_message(rvm, "not-valid-base64!") == {}


@pytest.mark.parametrize("rvm", PARALLAX_RVMS)
def test_every_decoder_handles_empty_payload(rvm: str) -> None:
    """An empty payload (every field at its proto3 default) never raises."""
    assert isinstance(decode_parallax_message(rvm, ""), dict)


def test_registered_rvms() -> None:
    """The public RVM lists match the registry."""
    assert PARALLAX_RVMS == list(RVMDecoder.decoders)
    assert set(CHARGING_RVMS) <= set(PARALLAX_RVMS)


def test_unknown_fields_and_enum_values_logged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Fields and enum values a schema doesn't define are logged, not dropped silently."""
    status = charging.SessionStatus(charging_state=30)  # type: ignore[arg-type]
    payload = status.SerializeToString() + b"\x78\x05"  # plus undeclared field 15 = 5
    with caplog.at_level(logging.DEBUG, logger="rivian.parallax.core"):
        result = decode_parallax_message(
            "charging.session.status", base64.b64encode(payload).decode()
        )
    assert result == {"chargerState": 30, "isActive": False}
    assert "SessionStatus: unknown field 15 (wire type 0) = 5" in caplog.text
    assert "SessionStatus.charging_state: unknown ChargingState value 30" in caplog.text


def test_duplicate_registration_rejected() -> None:
    """Registering a second decoder for an RVM raises."""
    with pytest.raises(ValueError):
        RVMDecoder.register("charging.session.status", charging.SessionStatus)(
            lambda _m: {}
        )
