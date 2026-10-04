"""Decoders for `security.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import security_pb2


@RVMDecoder.register("security.access.passive_entry", security_pb2.PassiveEntry)
def decode_passive_entry(_m: security_pb2.PassiveEntry) -> dict[str, Any]:
    """security.access.passive_entry — unmapped."""
    return {}


_ACCESS_CAN_FAULTED_MAP: Final[dict[int, str]] = {
    security_pb2.ACCESS_CAN_NO_FAILURE: "no_failure",
    security_pb2.ACCESS_CAN_FAILURE: "failure",
}

_ALARM_SOUND_MAP: Final[dict[int, str]] = {
    security_pb2.ALARM_SOUND_FALSE: "false",
    security_pb2.ALARM_SOUND_TRUE: "true",
    security_pb2.ALARM_SOUND_SIGNAL_NOT_AVAILABLE: "signal_not_available",
}

_HARDWARE_FAILURE_MAP: Final[dict[int, str]] = {
    security_pb2.HARDWARE_FAILURE_UNSPECIFIED: "unspecified",
    security_pb2.HARDWARE_FAILURE_SET: "set",
}

_IMMOBILIZER_MAP: Final[dict[int, str]] = {
    security_pb2.IMMOBILIZER_NOT_ASSIGNED: "not_assigned",
    security_pb2.IMMOBILIZER_NOT_AUTHORIZED: "not_authorized",
    security_pb2.IMMOBILIZER_AUTHORIZED_TO_DRIVE: "authorized_to_drive",
}

_PASSIVE_ENTRY_FAIL_MAP: Final[dict[int, str]] = {
    security_pb2.PASSIVE_ENTRY_NOT_IN_PARK: "not_in_park",
    security_pb2.PASSIVE_ENTRY_AT_HOME_DISABLE: "at_home_disable",
    security_pb2.PASSIVE_ENTRY_PASSENGER_IN_SEAT: "passenger_in_seat",
    security_pb2.PASSIVE_ENTRY_DEVICE_NOT_ENABLED: "device_not_enabled",
    security_pb2.PASSIVE_ENTRY_TRANSPORT_MODE: "transport_mode",
    security_pb2.PASSIVE_ENTRY_CAR_WASH_MODE: "car_wash_mode",
    security_pb2.PASSIVE_ENTRY_CAMP_MODE: "camp_mode",
    security_pb2.PASSIVE_ENTRY_ACTIVE_OTA: "active_ota",
    security_pb2.PASSIVE_ENTRY_SHOW_AND_TELL_MODE: "show_and_tell_mode",
    security_pb2.PASSIVE_ENTRY_RCVD_RSSI_PENDING: "rcvd_rssi_pending",
    security_pb2.PASSIVE_ENTRY_LOCK_ONLY_AT_HOME: "lock_only_at_home",
    security_pb2.PASSIVE_ENTRY_CAR_COSTUME_MODE: "car_costume_mode",
    security_pb2.PASSIVE_ENTRY_SLEPT_IMMEDIATE: "slept_immediate",
}

_SECURE_ELEMENT_FAULTED_MAP: Final[dict[int, str]] = {
    security_pb2.SECURE_ELEMENT_NO_FAILURE: "no_failure",
    security_pb2.SECURE_ELEMENT_LOST_COMMUNICATION: "lost_communication",
    security_pb2.SECURE_ELEMENT_APPLET_NOT_PROGRAMMED: "applet_not_programmed",
    security_pb2.SECURE_ELEMENT_NOT_CONFIGURED: "not_configured",
    security_pb2.SECURE_ELEMENT_ATTACK_COUNTER: "attack_counter",
    security_pb2.SECURE_ELEMENT_URSK_DECRYPT_FAILURE: "ursk_decrypt_failure",
}

_TOS_ACCEPTANCE_MAP: Final[dict[int, str]] = {
    security_pb2.TOS_NOT_ACCEPTED: "not_accepted",
    security_pb2.TOS_ACCEPTED: "accepted",
}

_VIDEO_MODE_MAP: Final[dict[int, str]] = {
    security_pb2.VIDEO_MODE_NONE: "none",
    security_pb2.VIDEO_MODE_EVERYWHERE: "everywhere",
    security_pb2.VIDEO_MODE_AWAY_FROM_HOME: "away_from_home",
}

_VIDEO_MONITORING_STATUS_MAP: Final[dict[int, str]] = {
    security_pb2.VIDEO_MONITORING_DISABLED: "disabled",
    security_pb2.VIDEO_MONITORING_ENABLED: "enabled",
    security_pb2.VIDEO_MONITORING_ACTIVE: "active",
}


# Btm field -> (result-key infix, log label).
_BTM_MODULES: Final = (
    ("ff", "Ff", "FF"),
    ("ic", "Ic", "IC"),
    ("lfd", "Lfd", "LFD"),
    ("rf", "Rf", "RF"),
    ("rfd", "Rfd", "RFD"),
    ("oc", "Oc", "OC"),
)


@RVMDecoder.register("security.access.btm", security_pb2.Btm)
def decode_btm_diagnosis(m: security_pb2.Btm) -> dict[str, Any]:
    """security.access.btm — hardware failure status per BTM module.

    Fields:
        btmFfHardwareFailureStatus, btmIcHardwareFailureStatus,
        btmLfdHardwareFailureStatus, btmRfHardwareFailureStatus,
        btmRfdHardwareFailureStatus, btmOcHardwareFailureStatus: str
    """
    return {
        f"btm{key}HardwareFailureStatus": _enum(
            _HARDWARE_FAILURE_MAP,
            _present(m, field),
            what=f"BTM {label} hardware failure",
        )
        for field, key, label in _BTM_MODULES
    }


@RVMDecoder.register("security.access.immobilizer_state", security_pb2.ImmobilizerState)
def decode_immobilizer_state(m: security_pb2.ImmobilizerState) -> dict[str, Any]:
    """security.access.immobilizer_state — immobilizer authorization state.

    Fields:
        secureImmobilizerStatus: str
    """
    return {
        "secureImmobilizerStatus": _enum(
            _IMMOBILIZER_MAP, _present(m, "status"), what="immobilizer state"
        )
    }


@RVMDecoder.register(
    "security.access.passive_entry_debug", security_pb2.PassiveEntryDebug
)
def decode_passive_entry_debug(m: security_pb2.PassiveEntryDebug) -> dict[str, Any]:
    """security.access.passive_entry_debug — why the last passive unlock failed.

    Fields:
        passiveEntryUnlockFailReason: str
    """
    return {
        "passiveEntryUnlockFailReason": _enum(
            _PASSIVE_ENTRY_FAIL_MAP,
            _present(m, "reason"),
            what="passive entry unlock fail reason",
        )
    }


@RVMDecoder.register("security.access.vas_fault", security_pb2.VasFault)
def decode_vas_fault(m: security_pb2.VasFault) -> dict[str, Any]:
    """security.access.vas_fault — vehicle access system fault status.

    Fields:
        vasSecureElementFaulted: str
        vasAccessCanFaulted: str
    """
    return {
        "vasSecureElementFaulted": _enum(
            _SECURE_ELEMENT_FAULTED_MAP,
            _present(m, "secure_element"),
            what="VAS secure element fault",
        ),
        "vasAccessCanFaulted": _enum(
            _ACCESS_CAN_FAULTED_MAP,
            _present(m, "access_can"),
            what="VAS access CAN fault",
        ),
    }


@RVMDecoder.register("security.alarm.state", security_pb2.AlarmState)
def decode_alarm_state(m: security_pb2.AlarmState) -> dict[str, Any]:
    """security.alarm.state — alarm sound status and disable notifications.

    Fields:
        alarmSoundStatus: str ("true" | "false" | "signal_not_available")
        consecutiveAlarmDisabledNotification: int — field mapping is a guess
    """
    return {
        "alarmSoundStatus": _enum(
            _ALARM_SOUND_MAP, _present(m, "sound_status"), what="alarm sound status"
        ),
        "consecutiveAlarmDisabledNotification": (
            m.consecutive_alarm_disabled_notification
        ),
    }


@RVMDecoder.register(
    "security.video_monitoring.state", security_pb2.VideoMonitoringState
)
def decode_video_monitoring(m: security_pb2.VideoMonitoringState) -> dict[str, Any]:
    """security.video_monitoring.state — GearGuard video monitoring status.

    Fields:
        gearGuardVideoStatus: str ("disabled" | "enabled" | "active");
            "active" while the vehicle is locked
        gearGuardVideoMode: str
        gearGuardVideoTermsAccepted: str
    """
    return {
        "gearGuardVideoStatus": _enum(
            _VIDEO_MONITORING_STATUS_MAP,
            _present(m, "status"),
            what="GearGuard video status",
        ),
        "gearGuardVideoMode": _enum(
            _VIDEO_MODE_MAP, _present(m, "mode"), what="GearGuard video mode"
        ),
        "gearGuardVideoTermsAccepted": _enum(
            _TOS_ACCEPTANCE_MAP,
            _present(m, "terms_accepted"),
            what="GearGuard video terms acceptance",
        ),
    }
