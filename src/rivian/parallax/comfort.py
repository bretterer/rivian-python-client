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
    return {"hvacTargetTemperature": round(m.target_temperature, 1)}


@RVMDecoder.register("comfort.user_modes.state", comfort_pb2.UserModesState)
def decode_user_modes_state(m: comfort_pb2.UserModesState) -> dict[str, Any]:
    """comfort.user_modes.state — user modes.

    Fields:
        serviceMode, carWashMode: str ("on" | "off")
        _petMode, _campMode, _transportMode, _climateKeep, _factoryMode:
            int — raw; enum types unknown
    """
    return {
        "serviceMode": "on" if m.in_service else "off",
        "carWashMode": "on" if m.car_wash_mode else "off",
        "_petMode": m.pet_mode,
        "_campMode": m.camp_mode,
        "_transportMode": m.transport_mode,
        "_climateKeep": m.climate_keep,
        "_factoryMode": m.factory_mode,
    }


_CLIMATE_HOLD_AVAILABILITY_MAP: Final[dict[int, str]] = {
    comfort_pb2.CLIMATE_HOLD_AVAILABILITY_UNSPECIFIED: "unspecified",
    comfort_pb2.CLIMATE_HOLD_AVAILABLE: "available",
    comfort_pb2.CLIMATE_HOLD_CONTROLLABLE: "controllable",
    comfort_pb2.CLIMATE_HOLD_UNAVAILABLE: "unavailable",
}

_CLIMATE_HOLD_STATUS_MAP: Final[dict[int, str]] = {
    comfort_pb2.CLIMATE_HOLD_STATUS_UNSPECIFIED: "unspecified",
    comfort_pb2.CLIMATE_HOLD_STATUS_UNAVAILABLE: "unavailable",
    comfort_pb2.CLIMATE_HOLD_STATUS_OFF: "off",
    comfort_pb2.CLIMATE_HOLD_STATUS_ON: "on",
    comfort_pb2.CLIMATE_HOLD_STATUS_FAULT: "fault",
}

_CLIMATE_HOLD_UNAVAILABILITY_REASON_MAP: Final[dict[int, str]] = {
    comfort_pb2.CLIMATE_HOLD_UNAVAILABILITY_UNSPECIFIED: "unspecified",
    comfort_pb2.CLIMATE_HOLD_UNAVAILABILITY_UNKNOWN: "unknown",
    comfort_pb2.CLIMATE_HOLD_UNAVAILABILITY_LOW_SOC: "low_soc",
    comfort_pb2.CLIMATE_HOLD_UNAVAILABILITY_FAULT: "fault",
}

_DEFROST_MAP: Final[dict[int, str]] = {
    comfort_pb2.DEFROST_DEFOG: "Defog",
    comfort_pb2.DEFROST_ACTIVE: "Defrost",
    comfort_pb2.DEFROST_DEFOG_DEFROST: "Defog_Defrost",
    comfort_pb2.DEFROST_OFF: "Off",
}

# GraphQL's cabinPreconditioningStatus / cabinPreconditioningType values.
_PRECONDITIONING_STATUS_MAP: Final[dict[int, str]] = {
    comfort_pb2.PRECONDITIONING_STATUS_UNSPECIFIED: "undefined",
    comfort_pb2.PRECONDITIONING_INITIATE: "initiate",
    comfort_pb2.PRECONDITIONING_ACTIVE: "active",
    comfort_pb2.PRECONDITIONING_ACTIVE_WARNING: "active_warning",
    comfort_pb2.PRECONDITIONING_COMPLETE_MAINTAIN: "complete_maintain",
    comfort_pb2.PRECONDITIONING_TIMEOUT_TEMP_NOT_ACHIEVED: (
        "timeout_temperature_not_achieved"
    ),
    comfort_pb2.PRECONDITIONING_ERROR_SOC_LOW: "error_soc_low",
    comfort_pb2.PRECONDITIONING_ERROR_SYSTEM_FAULT: "error_system_fault",
    comfort_pb2.PRECONDITIONING_UNAVAILABLE: "unavailable",
    comfort_pb2.PRECONDITIONING_TIMEOUT_COMPLETE: "timeout_complete",
}

_PRECONDITIONING_TYPE_MAP: Final[dict[int, str]] = {
    comfort_pb2.PRECONDITIONING_TYPE_USER_SELECTED: "user_selected",
    comfort_pb2.PRECONDITIONING_TYPE_SCREEN_PROTECTION: "screen_protection",
    comfort_pb2.PRECONDITIONING_TYPE_SCHEDULED: "scheduled",
    comfort_pb2.PRECONDITIONING_TYPE_AUTO_CABIN_VENTILATION: "auto_cabin_ventilation",
}

_PET_MODE_CABIN_CLIMATE_MAP: Final[dict[int, str]] = {
    comfort_pb2.PET_MODE_CABIN_CLIMATE_COMFORTABLE: "comfortable",
    comfort_pb2.PET_MODE_CABIN_CLIMATE_COLD: "cold",
    comfort_pb2.PET_MODE_CABIN_CLIMATE_HOT: "hot",
}

_PET_MODE_STATE_MAP: Final[dict[int, str]] = {
    comfort_pb2.PET_MODE_OFF: "off",
    comfort_pb2.PET_MODE_ON: "on",
    comfort_pb2.PET_MODE_DISABLED: "disabled",
    comfort_pb2.PET_MODE_FAULTY: "faulty",
}

_PET_MODE_TEMPERATURE_MAP: Final[dict[int, str]] = {
    comfort_pb2.PET_MODE_TEMPERATURE_DEFAULT: "default",
    comfort_pb2.PET_MODE_TEMPERATURE_COLD: "cold",
    comfort_pb2.PET_MODE_TEMPERATURE_HOT: "hot",
    comfort_pb2.PET_MODE_TEMPERATURE_FAULTY: "faulty",
}

# Seat keys use the GraphQL names: row 1 is "Front", row 2 "Rear", row 3
# "ThirdRow".
_CABIN_SURFACE_MAP: Final[dict[int, str]] = {
    comfort_pb2.STEERING_WHEEL: "steeringWheel",
    comfort_pb2.REAR_GLASS: "rearGlass",
    comfort_pb2.FRONT_GLASS: "frontGlass",
    comfort_pb2.SIDEVIEW_MIRRORS: "sideviewMirrors",
    comfort_pb2.SEAT_ROW_1_LEFT: "seatFrontLeft",
    comfort_pb2.SEAT_ROW_1_MIDDLE: "seatFrontMiddle",
    comfort_pb2.SEAT_ROW_1_RIGHT: "seatFrontRight",
    comfort_pb2.SEAT_ROW_2_LEFT: "seatRearLeft",
    comfort_pb2.SEAT_ROW_2_MIDDLE: "seatRearMiddle",
    comfort_pb2.SEAT_ROW_2_RIGHT: "seatRearRight",
    comfort_pb2.SEAT_ROW_3_LEFT: "seatThirdRowLeft",
    comfort_pb2.SEAT_ROW_3_MIDDLE: "seatThirdRowMiddle",
    comfort_pb2.SEAT_ROW_3_RIGHT: "seatThirdRowRight",
    comfort_pb2.WIPER_AREA: "wiperArea",
}

_CONDITIONING_LEVEL_MAP: Final[dict[int | None, str]] = {
    None: "Off",
    comfort_pb2.CONDITIONING_LEVEL_1: "Level_1",
    comfort_pb2.CONDITIONING_LEVEL_2: "Level_2",
    comfort_pb2.CONDITIONING_LEVEL_3: "Level_3",
}

_CONDITIONING_TYPE_MAP: Final[dict[int, str]] = {
    comfort_pb2.CONDITIONING_HEAT: "Heat",
    comfort_pb2.CONDITIONING_VENT: "Vent",
}


@RVMDecoder.register(
    "comfort.cabin.cabin_preconditioning_status", comfort_pb2.CabinPreconditioningStatus
)
def decode_preconditioning(m: comfort_pb2.CabinPreconditioningStatus) -> dict[str, Any]:
    """comfort.cabin.cabin_preconditioning_status — cabin preconditioning state.

    Fields:
        cabinPreconditioningStatus: str ("undefined" | "initiate" | "active" |
            "complete_maintain" | "unavailable" | ...); "unavailable" while
            driving or in pet comfort
        cabinPreconditioningType: str | None ("user_selected" |
            "screen_protection" | "scheduled" | "auto_cabin_ventilation")
    """
    return {
        "cabinPreconditioningStatus": _enum(
            _PRECONDITIONING_STATUS_MAP, m.status, what="preconditioning status"
        ),
        "cabinPreconditioningType": _enum(
            _PRECONDITIONING_TYPE_MAP, m.type or None, what="preconditioning type"
        ),
    }


@RVMDecoder.register("comfort.cabin.cabin_temperatures", comfort_pb2.CabinTemperatures)
def decode_cabin_temperatures(m: comfort_pb2.CabinTemperatures) -> dict[str, Any]:
    """comfort.cabin.cabin_temperatures — interior temperature and driver set point.

    Fields:
        cabinClimateInteriorTemperature: float (°C)
        cabinClimateDriverTemperature: float (°C) — set point, same as
            `hvacTargetTemperature`
        cabinClimateExteriorTemperature: float (°C), when sent
    """
    result: dict[str, Any] = {
        "cabinClimateInteriorTemperature": round(m.interior_temperature, 1),
        "cabinClimateDriverTemperature": round(m.driver_set_point, 1),
    }
    if (v := _present(m, "exterior_temperature")) is not None:
        result["cabinClimateExteriorTemperature"] = round(v, 1)
    return result


@RVMDecoder.register(
    "comfort.cabin.cabin_ventilation_setting", comfort_pb2.CabinVentilationSetting
)
def decode_cabin_ventilation(m: comfort_pb2.CabinVentilationSetting) -> dict[str, Any]:
    """comfort.cabin.cabin_ventilation_setting — auto cabin ventilation.

    Fields:
        cabinVentilationEnabled: bool
    """
    return {"cabinVentilationEnabled": m.auto_cabin_ventilation_enabled}


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
        climateHoldUnavailabilityReason: str | None — None when unspecified
        climateHoldEndTime: int | None (epoch seconds; None unless a hold runs)
    """
    reason = _enum(
        _CLIMATE_HOLD_UNAVAILABILITY_REASON_MAP,
        m.unavailability_reason,
        what="climate hold unavailability reason",
    )
    return {
        "climateHoldStatus": _enum(
            _CLIMATE_HOLD_STATUS_MAP, m.status, what="climate hold status"
        ),
        "climateHoldAvailability": _enum(
            _CLIMATE_HOLD_AVAILABILITY_MAP,
            m.availability,
            what="climate hold availability",
        ),
        "climateHoldUnavailabilityReason": None if reason == "unspecified" else reason,
        "climateHoldEndTime": m.end_time.seconds or None,
    }


@RVMDecoder.register(
    "comfort.cabin.defrost_defog_status", comfort_pb2.DefrostDefogStatus
)
def decode_defrost_status(m: comfort_pb2.DefrostDefogStatus) -> dict[str, Any]:
    """comfort.cabin.defrost_defog_status — windshield defrost state.

    Fields:
        defrostDefogStatus: str | None ("Defog" | "Defrost" | "Defog_Defrost"
            | "Off")
    """
    return {
        "defrostDefogStatus": _enum(
            _DEFROST_MAP, m.status or None, what="defrost defog status"
        )
    }


@RVMDecoder.register("comfort.cabin.pet_mode_status", comfort_pb2.PetModeStatus)
def decode_pet_mode_status(m: comfort_pb2.PetModeStatus) -> dict[str, Any]:
    """comfort.cabin.pet_mode_status — pet mode and temperature status.

    Fields:
        petModeStatus: str — "disabled" while cabin climate is off, "off"
            while it runs without pet mode
        petModeTemperatureStatus: str
        petModeCabinClimate: str ("comfortable" | "cold" | "hot")

    Absent fields are their zero values ("off" / "default" / "comfortable").
    """
    return {
        "petModeStatus": _enum(_PET_MODE_STATE_MAP, m.status, what="pet mode status"),
        "petModeTemperatureStatus": _enum(
            _PET_MODE_TEMPERATURE_MAP,
            m.temperature_status,
            what="pet mode temperature status",
        ),
        "petModeCabinClimate": _enum(
            _PET_MODE_CABIN_CLIMATE_MAP, m.cabin_climate, what="pet mode cabin climate"
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
        plus <surface>Heat/Vent for any other surface sent (middle seats,
        rearGlass, frontGlass, sideviewMirrors, wiperArea)

    A surface sent without a state is off.
    """
    result: dict[str, Any] = {}
    for surface in m.surface:
        surface_id, hvac_type = surface.id, surface.type
        state_val = _present(surface, "state")
        if surface_id in _CABIN_SURFACE_MAP and hvac_type in _CONDITIONING_TYPE_MAP:
            key = f"{_CABIN_SURFACE_MAP[surface_id]}{_CONDITIONING_TYPE_MAP[hvac_type]}"
            result[key] = _CONDITIONING_LEVEL_MAP.get(state_val, state_val)
        else:
            _LOGGER.debug(
                "Unknown cabin surface %s (hvac_type %s; state %s)",
                surface_id,
                hvac_type,
                state_val,
            )
    return result
