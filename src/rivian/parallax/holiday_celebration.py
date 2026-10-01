"""Decoders for `holiday_celebration.*` RVM topics."""

from __future__ import annotations

from typing import Any

from .core import RVMDecoder, _present
from .proto import holiday_celebration_pb2


@RVMDecoder.register(
    "holiday_celebration.car_costume.holiday_celebration_enabled",
    holiday_celebration_pb2.HolidayCelebrationEnabled,
)
def decode_holiday_celebration_enabled(
    _m: holiday_celebration_pb2.HolidayCelebrationEnabled,
) -> dict[str, Any]:
    """holiday_celebration.car_costume.holiday_celebration_enabled — unmapped."""
    return {}


@RVMDecoder.register(
    "holiday_celebration.car_costume.settings",
    holiday_celebration_pb2.CarCostumeSettings,
)
def decode_car_costume_settings(
    m: holiday_celebration_pb2.CarCostumeSettings,
) -> dict[str, Any]:
    """holiday_celebration.car_costume.settings — unmapped; fields as raw `_fieldN`."""
    result: dict[str, Any] = {}
    for num in (1, 2, 3, 6, 7, 9, 11, 12):
        if (v := _present(m, f"field_{num}")) is not None:
            result[f"_field{num}"] = v
    return result


@RVMDecoder.register(
    "holiday_celebration.car_costume.state", holiday_celebration_pb2.CarCostumeState
)
def decode_car_costume_state(
    m: holiday_celebration_pb2.CarCostumeState,
) -> dict[str, Any]:
    """holiday_celebration.car_costume.state — the current car costume.

    Fields:
        costumeId: int (0 = none; other ids unmapped)
    """
    if (v := _present(m, "costume_id")) is None:
        return {}
    return {"costumeId": v}


@RVMDecoder.register(
    "holiday_celebration.mobile_vehicle_settings.halloween_celebration_settings",
    holiday_celebration_pb2.HalloweenCelebrationSettings,
)
def decode_halloween_celebration_settings(
    m: holiday_celebration_pb2.HalloweenCelebrationSettings,
) -> dict[str, Any]:
    """holiday_celebration.mobile_vehicle_settings.halloween_celebration_settings — unmapped.

    Each field's wrapped value, when set, as a raw `_fieldN`.
    """
    result: dict[str, Any] = {}
    for num in (1, 2, 3, 4, 7, 8, 9, 10):
        field = f"field_{num}"
        if (
            m.HasField(field)
            and (v := _present(getattr(m, field), "value")) is not None
        ):
            result[f"_field{num}"] = v
    return result
