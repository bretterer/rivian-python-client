"""Decoders for `vehicle_access.*` RVM topics."""

from __future__ import annotations

from typing import Any

from .core import RVMDecoder
from .proto import vehicle_access_pb2


@RVMDecoder.register(
    "vehicle_access.state.passive_entry", vehicle_access_pb2.PassiveEntryState
)
def decode_vehicle_access_passive_entry(
    _m: vehicle_access_pb2.PassiveEntryState,
) -> dict[str, Any]:
    """vehicle_access.state.passive_entry — unmapped."""
    return {}
