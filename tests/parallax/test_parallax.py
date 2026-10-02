"""Tests for the `parallax.wakeup.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import parallax_pb2

from .helpers import decode, epoch


def test_heartbeat() -> None:
    """The heartbeat time plus raw unmapped values."""
    stamp = parallax_pb2.Heartbeat.Timestamp
    result = decode(
        "parallax.wakeup.heartbeat",
        parallax_pb2.Heartbeat(
            field_1=1,
            time=stamp(seconds=1790875649, nanos=500_000_000),
            field_3=stamp(seconds=1789473852),
        ),
    )
    assert result == {
        "heartbeatTime": epoch(1790875649_500),
        "_heartbeatField1": 1,
        "_heartbeatField3": epoch(1789473852_000),
    }
