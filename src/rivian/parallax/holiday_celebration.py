"""Decoders for `holiday_celebration.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from ..utils import from_epoch
from .core import RVMDecoder, _enum, _present
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


_COSTUME_EFFECT_TRIGGER_MAP: Final[dict[int, str]] = {
    holiday_celebration_pb2.COSTUME_EFFECT_TRIGGER_MANUAL: "manual",
    holiday_celebration_pb2.COSTUME_EFFECT_TRIGGER_MOTION: "motion",
}


@RVMDecoder.register(
    "holiday_celebration.car_costume.settings",
    holiday_celebration_pb2.CarCostumeSettings,
)
def decode_car_costume_settings(
    m: holiday_celebration_pb2.CarCostumeSettings,
) -> dict[str, Any]:
    """holiday_celebration.car_costume.settings — car costume settings.

    Names come from the app; the int values are unmapped enums.

    Fields:
        costumeSoundVolume: int
        costumeInteriorMusicEnabled: bool
        costumeInteriorMusicType: int
        costumeMotionExteriorLightSoundEffect: int
        costumeInteriorLightShowEnabled: bool
        costumeInteriorOverheadLightsEnabled: bool
        costumeLightsColor: int
        costumeEffect: int
        costumeEffectTrigger: str ("manual" | "motion"), None when unset
    """
    return {
        "costumeSoundVolume": m.celebration_sound_volume,
        "costumeInteriorMusicEnabled": m.interior_music_enabled,
        "costumeInteriorMusicType": m.interior_music_type,
        "costumeMotionExteriorLightSoundEffect": (m.motion_exterior_light_sound_effect),
        "costumeInteriorLightShowEnabled": m.interior_light_show_enabled,
        "costumeInteriorOverheadLightsEnabled": m.interior_overhead_lights_enabled,
        "costumeLightsColor": m.lights_color,
        "costumeEffect": m.costume_effect,
        "costumeEffectTrigger": (
            _enum(
                _COSTUME_EFFECT_TRIGGER_MAP,
                m.effect_trigger,
                what="costume effect trigger",
            )
            if m.effect_trigger
            else None
        ),
    }


@RVMDecoder.register(
    "holiday_celebration.car_costume.state", holiday_celebration_pb2.CarCostumeState
)
def decode_car_costume_state(
    m: holiday_celebration_pb2.CarCostumeState,
) -> dict[str, Any]:
    """holiday_celebration.car_costume.state — the current car costume.

    Names come from the app; the int values are unmapped enums.

    Fields:
        carCostumeAvailability: int
        costumeTheme: int
        costumeMotionTriggerDetected: bool
        activeCostumeEffect: int
        costumeStartTime: datetime, only when sent
    """
    result: dict[str, Any] = {
        "carCostumeAvailability": m.car_costume_availability,
        "costumeTheme": m.costume_theme,
        "costumeMotionTriggerDetected": m.motion_trigger_detected,
        "activeCostumeEffect": m.active_costume_effect,
    }
    if m.HasField("costume_start_time"):
        t = m.costume_start_time
        result["costumeStartTime"] = from_epoch(t.seconds + t.nanos / 1e9)
    return result


# Wrapped HalloweenCelebrationSettings field -> result key.
_HALLOWEEN_WRAPPED: Final = (
    ("sound_volume", "halloweenSoundVolume"),
    ("music_enabled", "halloweenMusicEnabled"),
    ("music_type", "halloweenMusicType"),
    ("sound_effect", "halloweenSoundEffect"),
    ("exterior_sounds_muted", "halloweenExteriorSoundsMuted"),
    ("light_show_enabled", "halloweenLightShowEnabled"),
    ("interior_overhead_lights_enabled", "halloweenInteriorOverheadLightsEnabled"),
    ("exterior_light_show_enabled", "halloweenExteriorLightShowEnabled"),
    ("lights_color", "halloweenLightsColor"),
    ("car_costume_availability", "halloweenCarCostumeAvailability"),
)


@RVMDecoder.register(
    "holiday_celebration.mobile_vehicle_settings.halloween_celebration_settings",
    holiday_celebration_pb2.HalloweenCelebrationSettings,
)
def decode_halloween_celebration_settings(
    m: holiday_celebration_pb2.HalloweenCelebrationSettings,
) -> dict[str, Any]:
    """holiday_celebration.mobile_vehicle_settings.halloween_celebration_settings.

    Names come from the app.

    Fields (each only when set):
        halloweenCostumeTheme: str
        halloweenSoundVolume: int
        halloweenMusicEnabled: bool
        halloweenMusicType: int
        halloweenSoundEffect: str
        halloweenExteriorSoundEffect: int
        halloweenExteriorSoundsMuted: bool
        halloweenLightShowEnabled: bool
        halloweenInteriorOverheadLightsEnabled: bool
        halloweenExteriorLightShowEnabled: bool
        halloweenLightsColor: str
        halloweenCarCostumeAvailability: str
        halloweenMotionLightSoundEnabled: bool
    """
    result: dict[str, Any] = {}
    if (
        m.HasField("costume_theme")
        and (v := _present(m.costume_theme, "theme_name")) is not None
    ):
        result["halloweenCostumeTheme"] = v
    for field, key in _HALLOWEEN_WRAPPED:
        if (
            m.HasField(field)
            and (v := _present(getattr(m, field), "value")) is not None
        ):
            result[key] = v
    for field, key in (
        ("exterior_sound_effect", "halloweenExteriorSoundEffect"),
        ("motion_light_sound_enabled", "halloweenMotionLightSoundEnabled"),
    ):
        if (v := _present(m, field)) is not None:
            result[key] = v
    return result
