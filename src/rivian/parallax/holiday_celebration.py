"""Decoders for `holiday_celebration.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

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

    Names come from the app; most fields have only been sent empty.

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
