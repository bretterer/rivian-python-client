"""Decoders for `comfort.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import _LOGGER, RVMDecoder, _enum, _present
from .proto import comfort_pb2


@RVMDecoder.register(
    "comfort.cabin.hvac_settings_status", comfort_pb2.HvacSettingsStatus
)
def decode_hvac_settings_status(m: comfort_pb2.HvacSettingsStatus) -> dict[str, Any]:
    """comfort.cabin.hvac_settings_status — target cabin temperature.

    Fields:
        hvacTargetTemperature: float (°C; 63.5 = "HI", set while defrosting)
    """
    if (v := _present(m, "target_temperature")) is None:
        return {}
    return {"hvacTargetTemperature": round(v, 1)}


@RVMDecoder.register("comfort.user_modes.state", comfort_pb2.UserModesState)
def decode_user_modes_state(m: comfort_pb2.UserModesState) -> dict[str, Any]:
    """comfort.user_modes.state — unmapped; fields 4 and 7 as `_field4`/`_field7`."""
    result: dict[str, Any] = {}
    if (v := _present(m, "field4")) is not None:
        result["_field4"] = v
    if (v := _present(m, "field7")) is not None:
        result["_field7"] = v
    return result


_CLIMATE_HOLD_AVAILABILITY_MAP: Final[dict[int, str]] = {
    0: "unspecified",
    1: "available",
    2: "controllable",
    3: "unavailable",
}

_CLIMATE_HOLD_STATUS_MAP: Final[dict[int, str]] = {
    0: "unspecified",
    1: "unavailable",
    2: "off",
    3: "on",
    4: "fault",
}

_CLIMATE_HOLD_UNAVAILABILITY_REASON_MAP: Final[dict[int, str]] = {
    0: "unspecified",
    1: "unknown",
    2: "low_soc",
}

_PET_MODE_STATE_MAP: Final[dict[int, str]] = {
    0: "off",
    1: "on",
    2: "disabled",
    3: "faulty",
}

_PET_MODE_TEMPERATURE_MAP: Final[dict[int, str]] = {
    0: "default",
    1: "cold",
    2: "hot",
    3: "faulty",
}

_SEAT_CONDITIONING_MAP: Final[dict[int, str]] = {
    1: "steeringWheel",
    5: "seatFrontLeft",
    7: "seatFrontRight",  # inferred
    8: "seatRearLeft",
    10: "seatRearRight",
    11: "seatThirdRowLeft",  # R1S
    13: "seatThirdRowRight",  # R1S
}

_SEAT_CONDITIONING_STATUS_MAP: Final[dict[int | None, str]] = {
    None: "Off",
    1: "Level_1",
    2: "Level_2",
    3: "Level_3",
}

_SEAT_CONDITIONING_TYPE_MAP: Final[dict[int, str]] = {
    1: "Heat",
    2: "Vent",
}


@RVMDecoder.register(
    "comfort.cabin.cabin_preconditioning_status", comfort_pb2.CabinPreconditioningStatus
)
def decode_preconditioning(m: comfort_pb2.CabinPreconditioningStatus) -> dict[str, Any]:
    """comfort.cabin.cabin_preconditioning_status — cabin preconditioning state.

    Fields:
        cabinPreconditioningStatus: str ("active" | "initiate" | "off");
            pet comfort counts as "active"
    """
    if m.status in (
        comfort_pb2.PRECONDITIONING_ACTIVE,
        comfort_pb2.PRECONDITIONING_PET_COMFORT,
    ):
        return {"cabinPreconditioningStatus": "active"}
    if m.status in (
        comfort_pb2.PRECONDITIONING_INITIATE_1,
        comfort_pb2.PRECONDITIONING_INITIATE_2,
    ):
        return {"cabinPreconditioningStatus": "initiate"}
    return {"cabinPreconditioningStatus": "off"}


@RVMDecoder.register("comfort.cabin.cabin_temperatures", comfort_pb2.CabinTemperatures)
def decode_cabin_temperatures(m: comfort_pb2.CabinTemperatures) -> dict[str, Any]:
    """comfort.cabin.cabin_temperatures — interior temperature and driver set point.

    Fields:
        cabinClimateInteriorTemperature: float (°C)
        cabinClimateDriverTemperature: float (°C) — set point, same as
            `hvacTargetTemperature`
    """
    result: dict[str, Any] = {}
    if (v := _present(m, "interior_temperature")) is not None:
        result["cabinClimateInteriorTemperature"] = round(v, 1)
    if (v := _present(m, "driver_set_point")) is not None:
        result["cabinClimateDriverTemperature"] = round(v, 1)
    return result


@RVMDecoder.register(
    "comfort.cabin.cabin_ventilation_setting", comfort_pb2.CabinVentilationSetting
)
def decode_cabin_ventilation(m: comfort_pb2.CabinVentilationSetting) -> dict[str, Any]:
    """comfort.cabin.cabin_ventilation_setting — passive ventilation settings.

    Fields (each only when sent):
        cabinVentilationEnabled: bool
        cabinVentilationMode: str ("AUTO" | "MANUAL" | "OFF")
        cabinVentilationWindowsPosition: int (percent open)
        cabinVentilationSunroofPosition: int (percent open)
        cabinVentilationDuration: int (minutes)
    """
    result: dict[str, Any] = {}
    for field, key in (
        ("enabled", "cabinVentilationEnabled"),
        ("mode", "cabinVentilationMode"),
        ("windows_position", "cabinVentilationWindowsPosition"),
        ("sunroof_position", "cabinVentilationSunroofPosition"),
        ("duration", "cabinVentilationDuration"),
    ):
        if (v := _present(m, field)) is not None:
            result[key] = v
    return result


@RVMDecoder.register(
    "comfort.cabin.climate_hold_setting", comfort_pb2.ClimateHoldSetting
)
def decode_climate_hold_setting(m: comfort_pb2.ClimateHoldSetting) -> dict[str, Any]:
    """comfort.cabin.climate_hold_setting — configured climate-hold duration.

    Fields:
        climateHoldDuration: int (seconds; 0 when no hold is set)
    """
    return {"climateHoldDuration": m.duration}


@RVMDecoder.register("comfort.cabin.climate_hold_status", comfort_pb2.ClimateHoldStatus)
def decode_climate_hold_status(m: comfort_pb2.ClimateHoldStatus) -> dict[str, Any]:
    """comfort.cabin.climate_hold_status — current climate-hold status.

    Fields:
        climateHoldStatus: str ("off" | "on" | "unavailable" | "fault" | "unspecified")
        climateHoldAvailability: str
        climateHoldUnavailabilityReason: str (only when not "unspecified")
        climateHoldEndTime: int (epoch seconds, only while a hold runs)
    """
    result: dict[str, Any] = {}
    if (val := _present(m, "status")) is not None:
        result["climateHoldStatus"] = _enum(
            _CLIMATE_HOLD_STATUS_MAP, val, what="climate hold status"
        )
    if (val := _present(m, "availability")) is not None:
        result["climateHoldAvailability"] = _enum(
            _CLIMATE_HOLD_AVAILABILITY_MAP, val, what="climate hold availability"
        )
    if (val := _present(m, "unavailability_reason")) is not None:
        reason = _enum(
            _CLIMATE_HOLD_UNAVAILABILITY_REASON_MAP,
            val,
            what="climate hold unavailability reason",
        )
        if reason != "unspecified":
            result["climateHoldUnavailabilityReason"] = reason
    if m.end_time.seconds:
        result["climateHoldEndTime"] = m.end_time.seconds
    return result


@RVMDecoder.register(
    "comfort.cabin.defrost_defog_status", comfort_pb2.DefrostDefogStatus
)
def decode_defrost_status(m: comfort_pb2.DefrostDefogStatus) -> dict[str, Any]:
    """comfort.cabin.defrost_defog_status — windshield defrost state.

    Fields:
        defrostDefogStatus: str ("Defrost" | "Off")
    """
    active = m.status == comfort_pb2.DEFROST_ACTIVE
    return {"defrostDefogStatus": "Defrost" if active else "Off"}


@RVMDecoder.register("comfort.cabin.pet_mode_status", comfort_pb2.PetModeStatus)
def decode_pet_mode_status(m: comfort_pb2.PetModeStatus) -> dict[str, Any]:
    """comfort.cabin.pet_mode_status — pet mode and temperature status.

    Fields:
        petModeStatus: str — "disabled" while cabin climate is off, "off"
            while it runs without pet mode
        petModeTemperatureStatus: str

    Absent fields are their zero values ("off" / "default").
    """
    return {
        "petModeStatus": _enum(_PET_MODE_STATE_MAP, m.status, what="pet mode status"),
        "petModeTemperatureStatus": _enum(
            _PET_MODE_TEMPERATURE_MAP,
            m.temperature_status,
            what="pet mode temperature status",
        ),
    }


@RVMDecoder.register(
    "comfort.cabin.seat_conditioning_status", comfort_pb2.SeatConditioningStatus
)
def decode_seat_conditioning(m: comfort_pb2.SeatConditioningStatus) -> dict[str, Any]:
    """comfort.cabin.seat_conditioning_status — seat and steering wheel heat/vent.

    Fields:
        seatFrontLeftHeat, seatFrontLeftVent, seatFrontRightHeat,
        seatFrontRightVent, seatRearLeftHeat, seatRearRightHeat,
        seatThirdRowLeftHeat, seatThirdRowRightHeat: str
            ("Off" | "Level_1" | "Level_2" | "Level_3")
        steeringWheelHeat: str ("Off" | "Level_1")

    Entries without a state are skipped.
    """
    result: dict[str, Any] = {}
    for s in m.seat:
        cid, hvac_type = s.id, s.type
        if (state_val := _present(s, "state")) is None:
            continue
        if cid in _SEAT_CONDITIONING_MAP and hvac_type in _SEAT_CONDITIONING_TYPE_MAP:
            key = (
                f"{_SEAT_CONDITIONING_MAP[cid]}{_SEAT_CONDITIONING_TYPE_MAP[hvac_type]}"
            )
            result[key] = _SEAT_CONDITIONING_STATUS_MAP.get(state_val, state_val)
        else:
            _LOGGER.debug(
                "Unknown seat conditioning status id %s (hvac_type %s; state %s)",
                cid,
                hvac_type,
                state_val,
            )
    return result
