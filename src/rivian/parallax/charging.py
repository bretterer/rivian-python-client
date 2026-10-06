"""Decoders for `charging.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from ..utils import from_epoch
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


_DERATE_STATUS_MAP: Final[dict[int, str]] = {
    charging_pb2.DERATE_STATUS_NONE: "none",
    charging_pb2.DERATE_STATUS_WARM_ADAPTER: "warm_adapter",
    charging_pb2.DERATE_STATUS_DC_WARM_PLUG: "dc_warm_plug",
    charging_pb2.DERATE_STATUS_AC_WARM_PLUG: "ac_warm_plug",
    charging_pb2.DERATE_STATUS_EVSE_DERATING: "evse_derating",
    charging_pb2.DERATE_STATUS_NEARING_TOC: "nearing_toc",
    charging_pb2.DERATE_STATUS_NEAR_TOC_LFP_BATT_CALIBRATING: "near_toc_lfp_batt_calibrating",
    charging_pb2.DERATE_STATUS_HVAC_PRIORITIZED: "hvac_prioritized",
    charging_pb2.DERATE_STATUS_BATTERY_HEATING: "battery_heating",
    charging_pb2.DERATE_STATUS_BATTERY_COOLING: "battery_cooling",
    charging_pb2.DERATE_STATUS_CELL_THERMAL_LIM_COLD_NO_CURRENT: "cell_thermal_lim_cold_no_current",
    charging_pb2.DERATE_STATUS_CELL_THERMAL_LIM_HOT_NO_CURRENT: "cell_thermal_lim_hot_no_current",
    charging_pb2.DERATE_STATUS_CELL_THERMAL_LIM_COLD: "cell_thermal_lim_cold",
    charging_pb2.DERATE_STATUS_CELL_THERMAL_LIM_HOT: "cell_thermal_lim_hot",
    charging_pb2.DERATE_STATUS_PACK_HARDWARE_THERMAL_LIM: "pack_hardware_thermal_lim",
    charging_pb2.DERATE_STATUS_HIGH_SOC_SIGMA: "high_soc_sigma",
    charging_pb2.DERATE_STATUS_HV_BATTERY_FAULT: "hv_battery_fault",
    charging_pb2.DERATE_STATUS_DCAC_EXPORT: "dcac_export",
}

_FAULT_CHIME_MAP: Final[dict[int, str]] = {
    charging_pb2.FAULT_CHIME_NONE: "none",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_ALL: "charging_disabled_all",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_DC: "charging_disabled_dc",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_DC: "charging_disabled_pin_temp_dc",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_GRADIENT_DC: "charging_disabled_pin_temp_gradient_dc",
    charging_pb2.FAULT_CHIME_CHARGING_DEGRADED_DC: "charging_degraded_dc",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_AC: "charging_disabled_ac",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_AC: "charging_disabled_pin_temp_ac",
    charging_pb2.FAULT_CHIME_CHARGING_DEGRADED_AC: "charging_degraded_ac",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_PARTIAL_CONNECTION: "charging_disabled_partial_connection",
    charging_pb2.FAULT_CHIME_CHARGING_DISABLED_NOT_PARKED: "charging_disabled_not_parked",
}


@RVMDecoder.register("charging.session.notification", charging_pb2.SessionNotification)
def decode_session_notification(m: charging_pb2.SessionNotification) -> dict[str, Any]:
    """charging.session.notification — charging derate and fault notices.

    Fields:
        chargerDerateStatus: str ("none" | "warm_adapter" | "nearing_toc" |
            "battery_heating" | ...)
        chargingFaultChime: str ("none" | "charging_disabled_all" |
            "charging_disabled_dc" | ...)
        _unexpectedStopReason: int — raw
    """
    return {
        "chargerDerateStatus": _enum(
            _DERATE_STATUS_MAP, m.derate_status, what="charger derate status"
        ),
        "chargingFaultChime": _enum(
            _FAULT_CHIME_MAP, m.fault_chime, what="charging fault chime"
        ),
        "_unexpectedStopReason": m.unexpected_stop_reason,
    }


# The same "true"/"false"/"signal_not_available" vocabulary as the alarm.
_START_AVAILABILITY_MAP: Final[dict[int, str]] = {
    charging_pb2.START_AVAILABILITY_SNA: "signal_not_available",
    charging_pb2.START_AVAILABILITY_FALSE: "false",
    charging_pb2.START_AVAILABILITY_TRUE: "true",
}

_TIME_ESTIMATION_VALIDITY_MAP: Final[dict[int, str]] = {
    charging_pb2.TIME_ESTIMATION_VALIDITY_VALID: "valid",
    charging_pb2.TIME_ESTIMATION_VALIDITY_INVALID: "invalid",
    charging_pb2.TIME_ESTIMATION_VALIDITY_PACK_DISCHARGING: "pack_discharging",
}


@RVMDecoder.register(
    "charging.session.remote_command", charging_pb2.SessionRemoteCommand
)
def decode_session_remote_command(
    m: charging_pb2.SessionRemoteCommand,
) -> dict[str, Any]:
    """charging.session.remote_command — whether a remote start is available.

    Fields:
        remoteChargingAvailable: str ("true" | "false" |
            "signal_not_available"); true while charging is held (e.g. by a
            schedule), so "charge now" can start it
    """
    return {
        "remoteChargingAvailable": _enum(
            _START_AVAILABILITY_MAP, m.start_available, what="remote charging"
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
    """charging.session.trip_target — the trip's target state of charge.

    Fields:
        chargingTripTargetSoc: int | None (percent; None when not set)
    """
    soc = m.soc_limit
    return {"chargingTripTargetSoc": None if soc in (0, 0xFFFF) else soc}


@RVMDecoder.register(
    "charging.smart_charging.settings", charging_pb2.SmartChargingSettings
)
def decode_smart_charging_settings(
    m: charging_pb2.SmartChargingSettings,
) -> dict[str, Any]:
    """charging.smart_charging.settings — smart charging schedule.

    Not seen yet; the schema comes from the app.

    Fields:
        smartChargingCleanEnergyEnabled: bool
        smartChargingReadyByTimes: list of {"hours": int, "minutes": int,
            "days": list[str]} ("monday" … "sunday")
    """
    return {
        "smartChargingCleanEnergyEnabled": m.clean_energy_enabled,
        "smartChargingReadyByTimes": [
            {
                "hours": t.hours,
                "minutes": t.minutes,
                "days": [
                    _enum(_SMART_CHARGING_DAY_MAP, d, what="smart charging day")
                    for d in t.days
                ],
            }
            for t in m.ready_by_times
        ],
    }


@RVMDecoder.register(
    "charging.smart_charging.smart_charging_info", charging_pb2.SmartChargingInfo
)
def decode_smart_charging_info(m: charging_pb2.SmartChargingInfo) -> dict[str, Any]:
    """charging.smart_charging.smart_charging_info — smart charging status.

    Not seen yet; the schema comes from the app.

    Fields:
        smartChargingNotification: str ("signal_not_available" |
            "charging_with_clean_energy" | "charging_paused" |
            "clean_energy_not_enough_time" |
            "clean_energy_forecast_unavailable_or_incomplete")
        smartChargingResumeTime: datetime, only when sent
        _smartChargingScheduleType: int (raw; unmapped)
    """
    result: dict[str, Any] = {
        "smartChargingNotification": _enum(
            _SMART_CHARGING_NOTIFICATION_MAP,
            m.notification,
            what="smart charging notification",
        ),
        "_smartChargingScheduleType": m.schedule_type,
    }
    if m.HasField("resume_time"):
        t = m.resume_time
        result["smartChargingResumeTime"] = from_epoch(t.seconds + t.nanos / 1e9)
    return result


@RVMDecoder.register(
    "charging.smart_charging.weighted_charging_forecast",
    charging_pb2.WeightedChargingForecast,
)
def decode_weighted_charging_forecast(
    _m: charging_pb2.WeightedChargingForecast,
) -> dict[str, Any]:
    """charging.smart_charging.weighted_charging_forecast — unmapped."""
    return {}


_SMART_CHARGING_DAY_MAP: Final[dict[int, str]] = {
    charging_pb2.SMART_CHARGING_DAY_MONDAY: "monday",
    charging_pb2.SMART_CHARGING_DAY_TUESDAY: "tuesday",
    charging_pb2.SMART_CHARGING_DAY_WEDNESDAY: "wednesday",
    charging_pb2.SMART_CHARGING_DAY_THURSDAY: "thursday",
    charging_pb2.SMART_CHARGING_DAY_FRIDAY: "friday",
    charging_pb2.SMART_CHARGING_DAY_SATURDAY: "saturday",
    charging_pb2.SMART_CHARGING_DAY_SUNDAY: "sunday",
}

_SMART_CHARGING_NOTIFICATION_MAP: Final[dict[int, str]] = {
    charging_pb2.SMART_CHARGING_NOTIFICATION_SNA: "signal_not_available",
    charging_pb2.SMART_CHARGING_NOTIFICATION_CHARGING_WITH_CLEAN_ENERGY: (
        "charging_with_clean_energy"
    ),
    charging_pb2.SMART_CHARGING_NOTIFICATION_CHARGING_PAUSED: "charging_paused",
    charging_pb2.SMART_CHARGING_NOTIFICATION_CLEAN_ENERGY_NOT_ENOUGH_TIME: (
        "clean_energy_not_enough_time"
    ),
    charging_pb2.SMART_CHARGING_NOTIFICATION_CLEAN_ENERGY_FORECAST_UNAVAILABLE_OR_INCOMPLETE: (
        "clean_energy_forecast_unavailable_or_incomplete"
    ),
}

_CONNECTION_STATE_MAP: Final[dict[int, str]] = {
    charging_pb2.CONNECTION_STATE_DISCONNECTED: "disconnected",
    charging_pb2.CONNECTION_STATE_CONNECTED: "connected",
    charging_pb2.CONNECTION_STATE_ERROR: "error",
    charging_pb2.CONNECTION_STATE_V2L_CONNECTED: "v2l_connected",
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
    charging_pb2.CHARGING_SMART_CHARGING_PAUSED: "smart_charging_paused",
    charging_pb2.CHARGING_SMART_CHARGING_ACTIVE: "smart_charging_active",
}


@RVMDecoder.register("charging.session.status", charging_pb2.SessionStatus)
def decode_charging_status(m: charging_pb2.SessionStatus) -> dict[str, Any]:
    """charging.session.status — plug and charging state.

    Fields:
        connectionState: str ("connected" | "disconnected" | "error" |
            "v2l_connected")
        chargerState: str — GraphQL chargerState values, e.g.
            "charging_ready" (no session, or unplugged),
            "charging_connecting", "charging_active", "charging_complete",
            "charging_scheduled", "charging_stopped_by_user"
        _evseType: int — raw; 1 while connected to a charger
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
    result["_evseType"] = m.evse_type
    return result


@RVMDecoder.register("charging.session.time_estimation", charging_pb2.TimeEstimation)
def decode_time_estimation(m: charging_pb2.TimeEstimation) -> dict[str, Any]:
    """charging.session.time_estimation — time to the charge limit.

    Fields:
        timeToEndOfCharge: int (minutes; 0 when not charging)
        chargingTimeEstimationValidity: str | None ("valid" | "invalid" |
            "pack_discharging")
    """
    return {
        "timeToEndOfCharge": m.estimated_time_remaining,
        "chargingTimeEstimationValidity": _enum(
            _TIME_ESTIMATION_VALIDITY_MAP,
            m.validity or None,
            what="time estimation validity",
        ),
    }


_CHARGER_STATUS_MAP: Final[dict[int, str]] = {
    charging_pb2.CHARGER_STATUS_NOT_CONNECTED: "chrgr_sts_not_connected",
    charging_pb2.CHARGER_STATUS_CONNECTED_NO_CHARGE: "chrgr_sts_connected_no_chrg",
    charging_pb2.CHARGER_STATUS_CONNECTED_CHARGING: "chrgr_sts_connected_charging",
}


@RVMDecoder.register("charging.energy.state", charging_pb2.EnergyState)
def decode_energy_state(m: charging_pb2.EnergyState) -> dict[str, Any]:
    """charging.energy.state — charger connection and charging state.

    Partial updates, so each field only when sent; most messages carry only
    power (not reported; charging.session.power has it). charging.session.status
    is the reliable source for the connection and charging states.

    Fields:
        chargerStatus: str — GraphQL chargerStatus values
            ("chrgr_sts_not_connected" | "chrgr_sts_connected_no_chrg" |
            "chrgr_sts_connected_charging"); inferred. Only sent when the
            plug state changes on some vehicles
        energyChargerState, energyConnectionState: str — as
            charging.session.status's chargerState / connectionState, which
            these can lag
        _field3: int — raw
    """
    result: dict[str, Any] = {}
    if (v := _present(m, "charging_state")) is not None:
        result["energyChargerState"] = _enum(
            _CHARGING_STATE_MAP, v, what="charging state"
        )
    if (v := _present(m, "connection_state")) is not None:
        result["energyConnectionState"] = _enum(
            _CONNECTION_STATE_MAP, v, what="charging connection state"
        )
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
