"""Tests for the `charging.*` and charging-graph decoders."""

from __future__ import annotations

import pytest

from rivian.parallax.proto import charging_pb2 as charging

from .helpers import decode


def test_schedule_time_window() -> None:
    """A configured window decodes days, times, amps, and location."""
    schedule = charging.ScheduleTimeWindow
    result = decode(
        "charging.schedule.time_window",
        schedule(
            enabled=True,
            window=schedule.Window(
                start_time=1320,
                end_time=900,
                duration=1020,
                amps=48,
                location=schedule.GeoCoordinate(latitude=33.5, longitude=-80.9),
                start_day=schedule.TUESDAY,
                end_day=schedule.WEDNESDAY,
            ),
        ),
    )
    assert result == {
        "chargingScheduleEnabled": True,
        "chargingScheduleStartDay": "tuesday",
        "chargingScheduleEndDay": "wednesday",
        "chargingScheduleStartTime": 1320,
        "chargingScheduleEndTime": 900,
        "chargingScheduleDuration": 1020,
        "chargingScheduleAmps": 48,
        "chargingScheduleLocation": {"latitude": 33.5, "longitude": -80.9},
    }


def test_schedule_time_window_defaults() -> None:
    """No schedule reads as disabled; an all-day window's midnight start is 0."""
    assert decode("charging.schedule.time_window") == {"chargingScheduleEnabled": False}

    schedule = charging.ScheduleTimeWindow
    result = decode(
        "charging.schedule.time_window",
        schedule(
            enabled=True,
            window=schedule.Window(
                end_time=1440,
                duration=10080,
                start_day=schedule.SUNDAY,
                end_day=schedule.SATURDAY,
            ),
        ),
    )
    assert result["chargingScheduleStartTime"] == 0
    assert result["chargingScheduleStartDay"] == "sunday"
    assert result["chargingScheduleEndDay"] == "saturday"


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (charging.CHARGING_READY, "charging_ready"),
        (charging.CHARGING_CONNECTING, "charging_connecting"),
        (charging.CHARGING_ACTIVE, "charging_active"),
        (charging.CHARGING_COMPLETE, "charging_complete"),
        (charging.CHARGING_SCHEDULED, "charging_scheduled"),
        (charging.CHARGING_USER_STOPPED, "charging_stopped_by_user"),
    ],
)
def test_session_status_phase(state: int, expected: str) -> None:
    """Every schema state maps to its decoder string."""
    result = decode(
        "charging.session.status",
        charging.SessionStatus(
            connection_state=charging.CONNECTION_STATE_CONNECTED,
            charging_state=state,  # type: ignore[arg-type]
            is_active=True,
        ),
    )
    assert result == {
        "connectionState": "connected",
        "chargerState": expected,
        "isActive": True,
    }


def test_session_status_unplugged() -> None:
    """Unplugged: disconnected, idle, and no session active."""
    result = decode(
        "charging.session.status",
        charging.SessionStatus(
            connection_state=charging.CONNECTION_STATE_DISCONNECTED,
            charging_state=charging.CHARGING_READY,
        ),
    )
    assert result == {
        "connectionState": "disconnected",
        "chargerState": "charging_ready",
        "isActive": False,
    }


def test_remote_command() -> None:
    """Start and stop commands."""
    rvm = "charging.session.remote_command"
    start = charging.SessionRemoteCommand(command=charging.REMOTE_COMMAND_START)
    stop = charging.SessionRemoteCommand(command=charging.REMOTE_COMMAND_STOP)
    assert decode(rvm, start) == {"chargingRemoteCommand": "start"}
    assert decode(rvm, stop) == {"chargingRemoteCommand": "stop"}


def test_time_estimation() -> None:
    """Minutes remaining; an empty payload means 0."""
    rvm = "charging.session.time_estimation"
    estimate = charging.TimeEstimation(estimated_time_remaining=91)
    assert decode(rvm, estimate) == {"timeToEndOfCharge": 91}
    assert decode(rvm) == {"timeToEndOfCharge": 0}


def test_energy_state() -> None:
    """Raw unmapped values."""
    result = decode(
        "charging.energy.state",
        charging.EnergyState(field_1=4, field_2=2, field_3=1, field_11=2),
    )
    assert result == {"_field1": 4, "_field2": 2, "_field3": 1, "_field11": 2}
