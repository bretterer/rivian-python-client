"""Decoders for `charging.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import charging_pb2

_DAY_OF_WEEK_MAP: Final[dict[int, str]] = {
    charging_pb2.ScheduleTimeWindow.SUNDAY: "sunday",
    charging_pb2.ScheduleTimeWindow.MONDAY: "monday",
    charging_pb2.ScheduleTimeWindow.TUESDAY: "tuesday",
    charging_pb2.ScheduleTimeWindow.WEDNESDAY: "wednesday",
    charging_pb2.ScheduleTimeWindow.THURSDAY: "thursday",
    charging_pb2.ScheduleTimeWindow.FRIDAY: "friday",
    charging_pb2.ScheduleTimeWindow.SATURDAY: "saturday",
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
    charging_pb2.REMOTE_COMMAND_START: "start",
    charging_pb2.REMOTE_COMMAND_STOP: "stop",
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
    charging_pb2.CONNECTION_STATE_DISCONNECTED: "disconnected",
    charging_pb2.CONNECTION_STATE_CONNECTED: "connected",
}

_CHARGING_STATE_MAP: Final[dict[int, str]] = {
    charging_pb2.CHARGING_READY: "charging_ready",
    charging_pb2.CHARGING_CONNECTING: "charging_connecting",
    charging_pb2.CHARGING_ACTIVE: "charging_active",
    charging_pb2.CHARGING_COMPLETE: "charging_complete",
    charging_pb2.CHARGING_SCHEDULED: "charging_scheduled",
    charging_pb2.CHARGING_VEHICLE_ERROR: "charging_vehicle_error",
    charging_pb2.CHARGING_STATION_ERROR: "charging_station_error",
    charging_pb2.CHARGING_USER_STOPPED: "charging_stopped_by_user",
    charging_pb2.CHARGING_STATION_STOPPED: "charging_stopped_by_station",
    charging_pb2.CHARGING_PAYMENT_ERROR: "charging_payment_error",
    charging_pb2.CHARGING_CERT_ERROR: "charging_cert_error",
    charging_pb2.CHARGING_TLS_ERROR: "charging_tls_error",
    charging_pb2.CHARGING_ERROR_AC_ADAPTER_USED_ON_DC: "charging_error_ac_adapter_used_on_dc",
    charging_pb2.CHARGING_ERROR_DC_ADAPTER_USED_ON_AC: "charging_error_dc_adapter_used_on_ac",
    charging_pb2.CHARGING_ERROR_INCOMPATIBLE_CHARGER: "charging_error_incompatible_charger",
    charging_pb2.CHARGING_SD_COMPENSATION: "charging_sd_compensation",
    charging_pb2.WAITING_ON_CHARGER: "waiting_on_charger",
    charging_pb2.CHARGER_NOT_READY_OR_INCOMPATIBLE: "charging_error_not_ready_or_incompatible_charger",
    charging_pb2.CHARGING_VEHICLE_STOPPED: "charging_vehicle_stopped",
    charging_pb2.CHARGING_PAYMENT_ERROR_START_RIVIAN_APP: "charging_payment_error_start_rivian_app",
    charging_pb2.CHARGING_TLS_ERROR_UNKNOWN_CHARGER: "charging_tls_error_unknown_charger",
    charging_pb2.CHARGING_TLS_ERROR_UNEXPECTED_FAIL: "charging_tls_error_unexpected_fail",
    charging_pb2.CHARGING_TLS_ERROR_START_RIVIAN_APP: "charging_tls_error_start_rivian_app",
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


_CHARGER_STATUS_MAP: Final[dict[int, str]] = {
    charging_pb2.CHARGER_STATUS_NOT_CONNECTED: "chrgr_sts_not_connected",
    charging_pb2.CHARGER_STATUS_CONNECTED_NO_CHARGE: "chrgr_sts_connected_no_chrg",
    charging_pb2.CHARGER_STATUS_CONNECTED_CHARGING: "chrgr_sts_connected_charging",
}


@RVMDecoder.register("charging.energy.state", charging_pb2.EnergyState)
def decode_energy_state(m: charging_pb2.EnergyState) -> dict[str, Any]:
    """charging.energy.state — charger connection and charging state.

    Fields:
        chargerStatus: str — GraphQL chargerStatus values
            ("chrgr_sts_not_connected" | "chrgr_sts_connected_no_chrg" |
            "chrgr_sts_connected_charging"); inferred
        chargerState, connectionState: str | None — as in
            charging.session.status
        _field3: int — raw
    """
    result: dict[str, Any] = {
        "chargerState": _enum(
            _CHARGING_STATE_MAP, m.charging_state or None, what="charging state"
        ),
        "connectionState": _enum(
            _CONNECTION_STATE_MAP,
            m.connection_state or None,
            what="charging connection state",
        ),
    }
    if (v := _present(m, "charger_status")) is not None:
        result["chargerStatus"] = _enum(_CHARGER_STATUS_MAP, v, what="charger status")
    if (v := _present(m, "field_3")) is not None:
        result["_field3"] = v
    return result


@RVMDecoder.register("charging.session.power", charging_pb2.SessionPower)
def decode_session_power(m: charging_pb2.SessionPower) -> dict[str, Any]:
    """charging.session.power — live charging power, about every 5 seconds.

    Fields:
        power: float (kW)

    Isn't resent as 0 when a charge completes, so gate on
    charging.session.status rather than treating the last value as live.
    """
    return {"power": round(m.power, 2)}
