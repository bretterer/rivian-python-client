"""Decoders for Rivian Parallax protobuf payloads.

Public API:
    decode_parallax_message(rvm, payload, timestamp=None, **kwargs) -> dict | None
        Adds `timestamp` (epoch milliseconds) as a UTC datetime if given.
    decode_parallax_subscription_message(data) -> dict | None
        Same, for a raw `subscribe_for_parallax_messages` message.
    PARALLAX_RVMS: list[str]  — every RVM with a registered decoder
    CHARGING_RVMS: list[str]  — the subset relevant to a charging session
    encode_vehicle_operation(rvm, payload=b"", ...) -> str
        Builds a `send_vehicle_operation` request; an empty payload reads
        the RVM, anything else (e.g. `encode_climate_hold_setting`) writes it.
    encode_command(vehicle_id, rvm, payload, ...) -> str
        Builds and signs a `send_parallax_command` request, with a payload
        such as `encode_unlock()`.
    LOCK_RVM / encode_lock(), UNLOCK_RVM / encode_unlock()
        The RVM and payload of a signed lock or unlock command.
    decode_command_state_message(data) -> dict | None
        Reads a raw `subscribe_for_parallax_command_state` message.
    encode_end_trip(user_id) -> str
        Builds the unsigned `end_trip` request.
    encode_live_streaming(camera, device_id) -> bytes
        A Gear Guard live stream start, for `start_gear_guard_live_stream`.
    encode_climate_hold(on), encode_pet_mode(on) -> bytes
        Payloads for the signed SET_CLIMATE_HOLD_RVM and SET_PET_MODE_RVM
        commands.
    encode_closures(closure), encode_cabin_surface(surface, conditioning, level),
    encode_defrost_defog(on), encode_preconditioning_temperature(celsius),
    encode_charge_limit(percent) -> bytes
        Payloads for signed body, comfort and charging commands; each command's
        RVM is a `*_RVM` constant.
    vehicle_command_feature(command) -> str | None
        The supported feature that, when AVAILABLE, sends a `VehicleCommand`
        over Parallax.
    encode_vehicle_command(command, params=None, *, model=None) -> (rvm, payload)
        The command's Parallax equivalent, for `send_parallax_command`.

Layout:
    core.py           - registry, payload parsing and shared helpers
    command.py        - signed remote commands and their state messages
    proto/            - .proto schemas and their generated *_pb2 modules
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
from .body import (
    CLOSE_CLOSURES_RVM,
    LOCK_RVM,
    OPEN_CLOSURES_RVM,
    UNLOCK_RVM,
    encode_closures,
    encode_lock,
    encode_unlock,
)
from .charging import (
    SET_CHARGE_LIMIT_RVM,
    START_CHARGING_RVM,
    STOP_CHARGING_RVM,
    encode_charge_limit,
)
from .comfort import (
    CLIMATE_HOLD_SETTING_RVM,
    CLIMATE_HOLD_STATUS_RVM,
    DISABLE_PRECONDITIONING_RVM,
    ENABLE_PRECONDITIONING_RVM,
    SET_CABIN_SURFACE_RVM,
    SET_CLIMATE_HOLD_RVM,
    SET_DEFROST_DEFOG_RVM,
    SET_PET_MODE_RVM,
    SET_PRECONDITIONING_TEMPERATURE_RVM,
    encode_cabin_surface,
    encode_climate_hold,
    encode_climate_hold_setting,
    encode_defrost_defog,
    encode_pet_mode,
    encode_preconditioning_temperature,
)
from .command import decode_command_state_message, encode_command
from .core import (
    RVMDecoder,
    decode_parallax_message,
    decode_parallax_subscription_message,
)
from .navigation import UPDATED_TRIP_MODEL, encode_end_trip
from .operation import encode_vehicle_operation
from .security import (
    DISABLE_PANIC_RVM,
    DISABLE_VIDEO_MONITORING_RVM,
    ENABLE_PANIC_RVM,
    ENABLE_VIDEO_MONITORING_RVM,
    GEAR_GUARD_CAMERAS,
    START_LIVE_STREAMING_RVM,
    encode_live_streaming,
)
from .vehicle_command import encode_vehicle_command, vehicle_command_feature

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
    "CLIMATE_HOLD_SETTING_RVM",
    "CLIMATE_HOLD_STATUS_RVM",
    "CLOSE_CLOSURES_RVM",
    "DISABLE_PANIC_RVM",
    "DISABLE_PRECONDITIONING_RVM",
    "DISABLE_VIDEO_MONITORING_RVM",
    "ENABLE_PANIC_RVM",
    "ENABLE_PRECONDITIONING_RVM",
    "ENABLE_VIDEO_MONITORING_RVM",
    "GEAR_GUARD_CAMERAS",
    "LOCK_RVM",
    "OPEN_CLOSURES_RVM",
    "PARALLAX_RVMS",
    "SET_CABIN_SURFACE_RVM",
    "SET_CHARGE_LIMIT_RVM",
    "SET_CLIMATE_HOLD_RVM",
    "SET_DEFROST_DEFOG_RVM",
    "SET_PET_MODE_RVM",
    "SET_PRECONDITIONING_TEMPERATURE_RVM",
    "START_CHARGING_RVM",
    "START_LIVE_STREAMING_RVM",
    "STOP_CHARGING_RVM",
    "UNLOCK_RVM",
    "UPDATED_TRIP_MODEL",
    "decode_command_state_message",
    "decode_parallax_message",
    "decode_parallax_subscription_message",
    "encode_cabin_surface",
    "encode_charge_limit",
    "encode_climate_hold",
    "encode_climate_hold_setting",
    "encode_closures",
    "encode_command",
    "encode_defrost_defog",
    "encode_end_trip",
    "encode_live_streaming",
    "encode_lock",
    "encode_pet_mode",
    "encode_preconditioning_temperature",
    "encode_unlock",
    "encode_vehicle_command",
    "encode_vehicle_operation",
    "vehicle_command_feature",
]
