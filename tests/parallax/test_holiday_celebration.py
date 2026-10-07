"""Tests for the `holiday_celebration.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import holiday_celebration_pb2 as holiday_celebration

from .helpers import decode, epoch


def test_halloween_celebration_settings() -> None:
    """Wrapped values are unwrapped; empty wrappers are left out."""
    settings = holiday_celebration.HalloweenCelebrationSettings
    result = decode(
        "holiday_celebration.mobile_vehicle_settings.halloween_celebration_settings",
        settings(
            costume_theme=settings.CostumeTheme(),
            sound_volume=settings.Int32Value(value=13),
            music_type=settings.Int32Value(value=1),
            exterior_sounds_muted=settings.BoolValue(value=True),
            lights_color=settings.Int32Value(),
        ),
    )
    assert result == {
        "halloweenSoundVolume": 13,
        "halloweenMusicType": 1,
        "halloweenExteriorSoundsMuted": True,
    }


def test_car_costume_settings() -> None:
    """Settings report every field, with zero values for absent ones."""
    result = decode(
        "holiday_celebration.car_costume.settings",
        holiday_celebration.CarCostumeSettings(
            celebration_sound_volume=7,
            interior_music_enabled=True,
            lights_color=2,
            effect_trigger=holiday_celebration.COSTUME_EFFECT_TRIGGER_MANUAL,
        ),
    )
    assert result == {
        "costumeSoundVolume": 7,
        "costumeInteriorMusicEnabled": True,
        "costumeInteriorMusicType": 0,
        "costumeMotionExteriorLightSoundEffect": 0,
        "costumeInteriorLightShowEnabled": False,
        "costumeInteriorOverheadLightsEnabled": False,
        "costumeLightsColor": 2,
        "costumeEffect": 0,
        "costumeEffectTrigger": "manual",
    }


def test_car_costume_state() -> None:
    """The start time is only reported when sent."""
    state = holiday_celebration.CarCostumeState
    rvm = "holiday_celebration.car_costume.state"
    result = decode(
        rvm,
        state(
            car_costume_availability=1,
            costume_theme=holiday_celebration.CAR_COSTUME_THEME_GHOSTBUSTERS,
            costume_start_time=state.Timestamp(seconds=1790553420),
        ),
    )
    assert result == {
        "carCostumeAvailability": 1,
        "costumeTheme": "ghostbusters",
        "costumeMotionTriggerDetected": False,
        "activeCostumeEffect": 0,
        "costumeStartTime": epoch(1790553420_000),
    }
    assert "costumeStartTime" not in decode(rvm)
