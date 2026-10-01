"""Decoders for `charging.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import charging_pb2

_DAY_OF_WEEK_MAP: Final[dict[int, str]] = {
    1: "sunday",
    2: "monday",
    3: "tuesday",
    4: "wednesday",
    5: "thursday",
    6: "friday",
    7: "saturday",
}


@RVMDecoder.register("charging.schedule.time_window", charging_pb2.ScheduleTimeWindow)
def decode_schedule_time_window(m: charging_pb2.ScheduleTimeWindow) -> dict[str, Any]:
    """charging.schedule.time_window — the scheduled charging window.

    Fields:
        chargingScheduleEnabled: bool — False when no schedule is set
        chargingScheduleStartDay, chargingScheduleEndDay: str
            ("sunday" ... "saturday")
        chargingScheduleStartTime, chargingScheduleEndTime: int — minutes
            after local midnight on that day (1440 = end of day)
        chargingScheduleDuration: int — minutes (10080 for all week)
        chargingScheduleAmps: int — current limit (A)
        chargingScheduleLocation: {"latitude": float, "longitude": float}

    The days are the window's current/next occurrence; its daily/weekdays
    recurrence isn't sent.
    """
    result: dict[str, Any] = {"chargingScheduleEnabled": m.enabled}
    if not m.HasField("window"):
        return result
    window = m.window
    result["chargingScheduleStartDay"] = _enum(
        _DAY_OF_WEEK_MAP, window.start_day or None, what="schedule start day"
    )
    result["chargingScheduleEndDay"] = _enum(
        _DAY_OF_WEEK_MAP, window.end_day or None, what="schedule end day"
    )
    result["chargingScheduleStartTime"] = window.start_time
    result["chargingScheduleEndTime"] = window.end_time
    result["chargingScheduleDuration"] = window.duration
    if window.HasField("amps"):
        result["chargingScheduleAmps"] = window.amps
    if window.HasField("location"):
        result["chargingScheduleLocation"] = {
            "latitude": round(window.location.latitude, 6),
            "longitude": round(window.location.longitude, 6),
        }
    return result


@RVMDecoder.register("charging.session.notification", charging_pb2.SessionNotification)
def decode_session_notification(m: charging_pb2.SessionNotification) -> dict[str, Any]:
    """charging.session.notification — unmapped; field 1 as `_field1`."""
    return {"_field1": m.field1} if m.HasField("field1") else {}


_REMOTE_COMMAND_MAP: Final[dict[int, str]] = {
    1: "start",
    2: "stop",
}


@RVMDecoder.register(
    "charging.session.remote_command", charging_pb2.SessionRemoteCommand
)
def decode_session_remote_command(
    m: charging_pb2.SessionRemoteCommand,
) -> dict[str, Any]:
    """charging.session.remote_command — the last start/stop command.

    Fields:
        chargingRemoteCommand: str ("start" | "stop")

    Also sent when the vehicle holds ("stop") or resumes ("start")
    charging around a schedule or limit change.
    """
    if not m.HasField("command"):
        return {}
    return {
        "chargingRemoteCommand": _enum(
            _REMOTE_COMMAND_MAP, m.command, what="charging remote command"
        )
    }


@RVMDecoder.register("charging.session.soc_slider", charging_pb2.SocSlider)
def decode_soc_slider(m: charging_pb2.SocSlider) -> dict[str, Any]:
    """charging.session.soc_slider — the charge limit.

    Fields:
        batteryLimit: int (percent, 0-100)
    """
    if not m.HasField("soc_limit"):
        return {}
    return {"batteryLimit": m.soc_limit}


@RVMDecoder.register("charging.session.trip_target", charging_pb2.TripTarget)
def decode_trip_target(m: charging_pb2.TripTarget) -> dict[str, Any]:
    """charging.session.trip_target — unmapped; field 2 as `_field2`.

    0xFFFF seems to mean "not set".
    """
    return {"_field2": m.field2} if m.HasField("field2") else {}


@RVMDecoder.register(
    "charging.smart_charging.settings", charging_pb2.SmartChargingSettings
)
def decode_smart_charging_settings(
    _m: charging_pb2.SmartChargingSettings,
) -> dict[str, Any]:
    """charging.smart_charging.settings — unmapped."""
    return {}


@RVMDecoder.register(
    "charging.smart_charging.smart_charging_info", charging_pb2.SmartChargingInfo
)
def decode_smart_charging_info(_m: charging_pb2.SmartChargingInfo) -> dict[str, Any]:
    """charging.smart_charging.smart_charging_info — unmapped."""
    return {}


@RVMDecoder.register(
    "charging.smart_charging.weighted_charging_forecast",
    charging_pb2.WeightedChargingForecast,
)
def decode_weighted_charging_forecast(
    _m: charging_pb2.WeightedChargingForecast,
) -> dict[str, Any]:
    """charging.smart_charging.weighted_charging_forecast — unmapped."""
    return {}


_CONNECTION_STATE_MAP: Final[dict[int, str]] = {
    1: "disconnected",
    2: "connected",
}

_CHARGING_STATE_MAP: Final[dict[int, str]] = {
    1: "charging_ready",
    2: "charging_connecting",
    3: "charging_active",
    4: "charging_complete",
    5: "charging_scheduled",
    6: "charging_vehicle_error",
    7: "charging_station_error",
    8: "charging_stopped_by_user",
    9: "charging_stopped_by_station",
    10: "charging_payment_error",
    11: "charging_cert_error",
    12: "charging_tls_error",
    13: "charging_error_ac_adapter_used_on_dc",
    14: "charging_error_dc_adapter_used_on_ac",
    15: "charging_error_incompatible_charger",
    16: "charging_sd_compensation",
    17: "waiting_on_charger",
    18: "charging_error_not_ready_or_incompatible_charger",
    19: "charging_vehicle_stopped",
    20: "charging_payment_error_start_rivian_app",
    21: "charging_tls_error_unknown_charger",
    22: "charging_tls_error_unexpected_fail",
    23: "charging_tls_error_start_rivian_app",
}


@RVMDecoder.register("charging.session.status", charging_pb2.SessionStatus)
def decode_charging_status(m: charging_pb2.SessionStatus) -> dict[str, Any]:
    """charging.session.status — plug and charging state.

    Fields:
        connectionState: str ("connected" | "disconnected")
        chargerState: str — GraphQL chargerState values, e.g.
            "charging_ready" (no session, or unplugged),
            "charging_connecting", "charging_active", "charging_complete",
            "charging_scheduled", "charging_stopped_by_user"
        isActive: bool — true from a session's start until it ends
    """
    result: dict[str, Any] = {}
    if m.HasField("connection_state"):
        result["connectionState"] = _enum(
            _CONNECTION_STATE_MAP, m.connection_state, what="charging connection state"
        )
    if m.HasField("charging_state"):
        result["chargerState"] = _enum(
            _CHARGING_STATE_MAP, m.charging_state, what="charging state"
        )
    result["isActive"] = m.is_active
    return result


@RVMDecoder.register("charging.session.time_estimation", charging_pb2.TimeEstimation)
def decode_time_estimation(m: charging_pb2.TimeEstimation) -> dict[str, Any]:
    """charging.session.time_estimation — time to the charge limit.

    Fields:
        timeToEndOfCharge: int (minutes; 0 when not charging)
    """
    return {"timeToEndOfCharge": m.estimated_time_remaining}


@RVMDecoder.register("charging.energy.state", charging_pb2.EnergyState)
def decode_energy_state(m: charging_pb2.EnergyState) -> dict[str, Any]:
    """charging.energy.state — unmapped; `_field1`-`_field3`, `_field11` raw."""
    return {
        f"_field{num}": v
        for num in (1, 2, 3, 11)
        if (v := _present(m, f"field_{num}")) is not None
    }


@RVMDecoder.register("charging.session.power", charging_pb2.SessionPower)
def decode_session_power(_m: charging_pb2.SessionPower) -> dict[str, Any]:
    """charging.session.power — unmapped; empty so far."""
    return {}
