"""Decoders for `departure.*` RVM topics."""

from __future__ import annotations

from typing import Any

from ..utils import from_epoch
from .core import RVMDecoder, _present
from .proto import departure_pb2

_Schedules = departure_pb2.DepartureSchedules

# Days field -> gateway WeekDay value.
_WEEKDAYS = (
    ("monday", "monday"),
    ("tuesday", "tuesday"),
    ("wednesday", "wednesday"),
    ("thursday", "thursday"),
    ("friday", "friday"),
    ("saturday", "saturday"),
    ("sunday", "sunday"),
)

_DEFOG_DEFROST = {
    departure_pb2.DEFOG_DEFROST_OFF: "off",
    departure_pb2.DEFOG_DEFROST_DEFOG: "defog",
    departure_pb2.DEFOG_DEFROST_DEFROST: "defrost",
}
_SURFACE_LEVEL = {
    departure_pb2.SURFACE_OFF: "off",
    departure_pb2.SURFACE_HEAT_1: "heat_1",
    departure_pb2.SURFACE_HEAT_2: "heat_2",
    departure_pb2.SURFACE_HEAT_3: "heat_3",
    departure_pb2.SURFACE_VENT_1: "vent_1",
    departure_pb2.SURFACE_VENT_2: "vent_2",
    departure_pb2.SURFACE_VENT_3: "vent_3",
}
_SURFACES = (
    ("front_left_seat", "frontLeftSeat"),
    ("front_right_seat", "frontRightSeat"),
    ("rear_left_seat", "rearLeftSeat"),
    ("rear_right_seat", "rearRightSeat"),
    ("steering_wheel", "steeringWheel"),
)


def _decode_schedule(schedule: _Schedules.Schedule) -> dict[str, Any]:
    """Decode one schedule into the gateway's DepartureSchedule shape."""
    entry: dict[str, Any] = {}
    if (v := _present(schedule, "id")) is not None:
        entry["id"] = v
    if (v := _present(schedule, "name")) is not None:
        entry["name"] = v
    entry["isEnabled"] = schedule.is_enabled

    occurrence = schedule.occurrence
    entry["occurrence"] = {
        "days": [day for field, day in _WEEKDAYS if getattr(occurrence.days, field)],
        "startsAtMin": occurrence.starts_at,
    }

    settings = schedule.departure_settings
    comfort = settings.comfort_settings
    levels = comfort.surface_heat_vent_levels
    entry["departureSettings"] = {
        "shouldOverrideChargeSchedule": settings.should_override_charge_schedule,
        "comfortSettings": {
            "cabinTempCelsius": round(comfort.cabin_temperature, 1),
            "frontDefogDefrost": _DEFOG_DEFROST.get(
                comfort.front_defog_defrost, comfort.front_defog_defrost
            ),
            "surfaceHeatVentLevels": {
                key: _SURFACE_LEVEL.get(level, level)
                for field, key in _SURFACES
                if (level := getattr(levels, field)) is not None
            },
        },
    }
    return entry


@RVMDecoder.register("departure.schedule.schedule", departure_pb2.DepartureSchedules)
def decode_departure_schedules(m: departure_pb2.DepartureSchedules) -> dict[str, Any]:
    """departure.schedule.schedule — departure (precondition) schedules.

    Fields:
        departureSchedules: list[dict] — the gateway's DepartureSchedule shape:
            id: str, name: str, isEnabled: bool
            occurrence: {"days": list[str] ("monday" ... "sunday"; order
                inferred), "startsAtMin": int (minutes after local midnight)}
            departureSettings: {"shouldOverrideChargeSchedule": bool,
                "comfortSettings": {"cabinTempCelsius": float,
                "frontDefogDefrost": "off" | "defog" | "defrost",
                "surfaceHeatVentLevels": {frontLeftSeat, frontRightSeat,
                rearLeftSeat, rearRightSeat, steeringWheel: "off" |
                "heat_1" ... "vent_3"}}}
        departureSchedulesUpdatedAt: datetime
    """
    result: dict[str, Any] = {
        "departureSchedules": [_decode_schedule(s) for s in m.schedule]
    }
    if m.HasField("updated_at"):
        seconds = m.updated_at.seconds + m.updated_at.nanos / 1e9
        result["departureSchedulesUpdatedAt"] = from_epoch(seconds)
    return result
