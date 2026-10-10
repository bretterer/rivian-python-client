"""Tests for the `departure.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import departure_pb2 as departure

from .helpers import decode, epoch

Schedules = departure.DepartureSchedules


def test_departure_schedules() -> None:
    """Schedules decode into the gateway's DepartureSchedule shape."""
    schedule = Schedules.Schedule(
        id="w-1",
        name="Weekdays",
        is_enabled=True,
        occurrence=Schedules.Occurrence(
            days=Schedules.Days(monday=True, friday=True), starts_at=540
        ),
        departure_settings=Schedules.DepartureSettings(
            should_override_charge_schedule=True,
            comfort_settings=Schedules.ComfortSettings(
                cabin_temperature=20.5,
                front_defog_defrost=departure.DEFOG_DEFROST_DEFROST,
                surface_heat_vent_levels=Schedules.SurfaceHeatVentLevels(
                    front_left_seat=departure.SURFACE_HEAT_3,
                    steering_wheel=departure.SURFACE_HEAT_1,
                ),
            ),
        ),
    )
    result = decode(
        "departure.schedule.schedule",
        Schedules(
            schedule=[schedule],
            updated_at=Schedules.UpdatedAt(seconds=1730877268),
        ),
    )
    assert result == {
        "departureSchedules": [
            {
                "id": "w-1",
                "name": "Weekdays",
                "isEnabled": True,
                "occurrence": {"days": ["monday", "friday"], "startsAtMin": 540},
                "departureSettings": {
                    "shouldOverrideChargeSchedule": True,
                    "comfortSettings": {
                        "cabinTempCelsius": 20.5,
                        "frontDefogDefrost": "defrost",
                        "surfaceHeatVentLevels": {
                            "frontLeftSeat": "heat_3",
                            "frontRightSeat": "off",
                            "rearLeftSeat": "off",
                            "rearRightSeat": "off",
                            "steeringWheel": "heat_1",
                        },
                    },
                },
            }
        ],
        "departureSchedulesUpdatedAt": epoch(1730877268_000),
    }


def test_departure_schedules_empty() -> None:
    """No schedules reads as an empty list."""
    assert decode("departure.schedule.schedule") == {"departureSchedules": []}
