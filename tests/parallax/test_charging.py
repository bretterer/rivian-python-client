"""Tests for the `charging.*` and charging-graph decoders."""

from __future__ import annotations

import pytest

from rivian.parallax.proto import charging_pb2 as charging

from .helpers import decode, epoch


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
            evse_type=1,
        ),
    )
    assert result == {
        "connectionState": "connected",
        "chargerState": expected,
        "_evseType": 1,
    }


def test_session_status_unplugged() -> None:
    """Unplugged: disconnected, ready, and no charger."""
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
        "_evseType": 0,
    }


def test_remote_command() -> None:
    """Whether a remote start is available; an empty payload is SNA."""
    rvm = "charging.session.remote_command"
    available = charging.SessionRemoteCommand(
        start_available=charging.START_AVAILABILITY_TRUE
    )
    assert decode(rvm, available) == {"remoteChargingAvailable": "true"}
    assert decode(rvm) == {"remoteChargingAvailable": "signal_not_available"}


def test_session_notification() -> None:
    """Derate and fault chime by name, plus the raw stop reason."""
    result = decode(
        "charging.session.notification",
        charging.SessionNotification(
            unexpected_stop_reason=1,
            derate_status=charging.DERATE_STATUS_BATTERY_HEATING,
            fault_chime=charging.FAULT_CHIME_CHARGING_DISABLED_AC,
        ),
    )
    assert result == {
        "chargerDerateStatus": "battery_heating",
        "chargingFaultChime": "charging_disabled_ac",
        "_unexpectedStopReason": 1,
    }


def test_time_estimation() -> None:
    """Minutes remaining; an empty payload means 0."""
    rvm = "charging.session.time_estimation"
    estimate = charging.TimeEstimation(
        validity=charging.TIME_ESTIMATION_VALIDITY_VALID, estimated_time_remaining=91
    )
    assert decode(rvm, estimate) == {
        "timeToEndOfCharge": 91,
        "chargingTimeEstimationValidity": "valid",
    }
    assert decode(rvm) == {
        "timeToEndOfCharge": 0,
        "chargingTimeEstimationValidity": None,
    }


def test_energy_state() -> None:
    """Charger status plus the session's charging and connection states."""
    result = decode(
        "charging.energy.state",
        charging.EnergyState(
            charging_state=charging.CHARGING_COMPLETE,
            charger_status=charging.CHARGER_STATUS_CONNECTED_NO_CHARGE,
            field_3=1,
            field_8=1,
            connection_state=charging.CONNECTION_STATE_CONNECTED,
        ),
    )
    assert result == {
        "energyChargerState": "charging_complete",
        "energyConnectionState": "connected",
        "chargerStatus": "chrgr_sts_connected_no_chrg",
        "_field3": 1,
        "_field8": 1,
    }


def test_energy_state_power_only() -> None:
    """A power-only update doesn't clear the states."""
    assert decode("charging.energy.state", charging.EnergyState(power=9.1)) == {}


def test_session_power() -> None:
    """Live power in kW, and 0 for the empty payload sent when not charging."""
    rvm = "charging.session.power"
    assert decode(rvm, charging.SessionPower(power=10.9)) == {
        "power": pytest.approx(10.9)
    }
    assert decode(rvm) == {"power": 0.0}


def test_trip_target() -> None:
    """The trip's target SoC, or None for the "not set" value."""
    rvm = "charging.session.trip_target"
    assert decode(rvm, charging.TripTarget(soc_limit=80)) == {
        "chargingTripTargetSoc": 80
    }
    assert decode(rvm, charging.TripTarget(soc_limit=0xFFFF)) == {
        "chargingTripTargetSoc": None
    }


def test_smart_charging_settings() -> None:
    """Ready-by times and the clean energy toggle."""
    settings = charging.SmartChargingSettings
    result = decode(
        "charging.smart_charging.settings",
        settings(
            ready_by_times=[
                settings.ReadyByTime(
                    hours=7,
                    minutes=30,
                    days=[
                        charging.SMART_CHARGING_DAY_MONDAY,
                        charging.SMART_CHARGING_DAY_SUNDAY,
                    ],
                )
            ],
            clean_energy_enabled=True,
        ),
    )
    assert result == {
        "smartChargingCleanEnergyEnabled": True,
        "smartChargingReadyByTimes": [
            {"hours": 7, "minutes": 30, "days": ["monday", "sunday"]}
        ],
    }


def test_smart_charging_info() -> None:
    """The notification, schedule type and resume time."""
    info = charging.SmartChargingInfo
    rvm = "charging.smart_charging.smart_charging_info"
    result = decode(
        rvm,
        info(
            resume_time=info.ResumeTime(seconds=1790553420),
            notification=charging.SMART_CHARGING_NOTIFICATION_CHARGING_PAUSED,
            schedule_type=1,
        ),
    )
    assert result == {
        "smartChargingNotification": "charging_paused",
        "_smartChargingScheduleType": 1,
        "smartChargingResumeTime": epoch(1790553420_000),
    }
    assert decode(rvm) == {
        "smartChargingNotification": "signal_not_available",
        "_smartChargingScheduleType": 0,
    }
