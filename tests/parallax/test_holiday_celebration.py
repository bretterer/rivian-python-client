"""Tests for the `holiday_celebration.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import holiday_celebration_pb2 as holiday_celebration

from .helpers import decode


def test_halloween_celebration_settings() -> None:
    """Wrapped values are surfaced raw; empty wrappers are left out."""
    settings = holiday_celebration.HalloweenCelebrationSettings
    result = decode(
        "holiday_celebration.mobile_vehicle_settings.halloween_celebration_settings",
        settings(
            field_1=settings.Value(),
            field_2=settings.Value(value=13),
            field_4=settings.Value(value=1),
        ),
    )
    assert result == {"_field2": 13, "_field4": 1}
