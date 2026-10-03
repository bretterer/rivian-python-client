"""Tests for the `holiday_celebration.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import holiday_celebration_pb2 as holiday_celebration

from .helpers import decode


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
            lights_color=settings.StringValue(),
        ),
    )
    assert result == {
        "halloweenSoundVolume": 13,
        "halloweenMusicType": 1,
        "halloweenExteriorSoundsMuted": True,
    }
