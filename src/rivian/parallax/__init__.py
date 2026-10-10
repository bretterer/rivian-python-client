"""Decoders for Rivian Parallax protobuf payloads.

Public API:
    decode_parallax_message(rvm, payload, timestamp=None, **kwargs) -> dict | None
        Adds `timestamp` (epoch milliseconds) as a UTC datetime if given.
    decode_parallax_subscription_message(data) -> dict | None
        Same, for a raw `subscribe_for_parallax_messages` message.
    PARALLAX_RVMS: list[str]  — every RVM with a registered decoder
    CHARGING_RVMS: list[str]  — the subset relevant to a charging session

Layout:
    core.py  - registry, payload parsing and shared helpers
    proto/   - .proto schemas and their generated *_pb2 modules
    <topic prefix>.py - one module per RVM topic prefix (body.*, etc.)

To add a decoder, decorate it with
`@RVMDecoder.register("the.rvm.topic", some_pb2.Message)` in its prefix's
module; a new module also needs adding to the import list below.
"""

from __future__ import annotations

from . import (  # noqa: F401  (imported to register their decoders)
    body,
    charging,
    comfort,
    departure,
    device_table,
    dynamics,
    energy,
    energy_edge_compute,
    gearguard_streaming,
    geofence,
    holiday_celebration,
    navigation,
    ota,
    parallax,
    secure_file_transfer,
    security,
    user_passcodes,
    vehicle,
    vehicle_access,
)
from .core import (
    RVMDecoder,
    decode_parallax_message,
    decode_parallax_subscription_message,
)

PARALLAX_RVMS: list[str] = list(RVMDecoder.decoders)

CHARGING_RVMS: list[str] = [
    "charging.energy.state",
    "charging.session.notification",
    "charging.session.power",
    "charging.session.remote_command",
    "charging.session.soc_slider",
    "charging.session.status",
    "charging.session.time_estimation",
    "energy.high_voltage.battery_state",
    "energy_edge_compute.graphs.charge_session_breakdown",
    "energy_edge_compute.graphs.charging_graph_global",
]

__all__ = [
    "CHARGING_RVMS",
    "PARALLAX_RVMS",
    "decode_parallax_message",
    "decode_parallax_subscription_message",
]
