"""Decoders for `parallax.*` RVM topics."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils import from_epoch
from .core import RVMDecoder, _present
from .proto import parallax_pb2


def _time(timestamp: parallax_pb2.Heartbeat.Timestamp) -> datetime:
    return from_epoch(timestamp.seconds + timestamp.nanos / 1e9)


@RVMDecoder.register("parallax.wakeup.heartbeat", parallax_pb2.Heartbeat)
def decode_heartbeat(m: parallax_pb2.Heartbeat) -> dict[str, Any]:
    """parallax.wakeup.heartbeat — a heartbeat sent when the vehicle wakes.

    Fields:
        heartbeatTime: datetime — send time (inferred)
        _heartbeatField1: int — unknown
        _heartbeatField3: datetime — an earlier time; unknown
    """
    result: dict[str, Any] = {}
    if m.HasField("time"):
        result["heartbeatTime"] = _time(m.time)
    if (v := _present(m, "field_1")) is not None:
        result["_heartbeatField1"] = v
    if m.HasField("field_3"):
        result["_heartbeatField3"] = _time(m.field_3)
    return result
