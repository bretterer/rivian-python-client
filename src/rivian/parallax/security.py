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
    1: "no_failure",
    2: "failure",
}

_ALARM_SOUND_MAP: Final[dict[int, str]] = {
    1: "false",
    2: "true",
    3: "signal_not_available",
}

_HARDWARE_FAILURE_MAP: Final[dict[int, str]] = {
    0: "unspecified",
    1: "set",
}

_IMMOBILIZER_MAP: Final[dict[int, str]] = {
    0: "not_assigned",
    1: "not_authorized",
    2: "authorized_to_drive",
}

_PASSIVE_ENTRY_FAIL_MAP: Final[dict[int, str]] = {
    1: "not_in_park",
    2: "at_home_disable",
    3: "passenger_in_seat",
    4: "device_not_enabled",
    5: "transport_mode",
    6: "car_wash_mode",
    7: "camp_mode",
    8: "active_ota",
    9: "show_and_tell_mode",
    10: "rcvd_rssi_pending",
    11: "lock_only_at_home",
    12: "car_costume_mode",
    13: "slept_immediate",
}

_SECURE_ELEMENT_FAULTED_MAP: Final[dict[int, str]] = {
    1: "no_failure",
    2: "lost_communication",
    3: "applet_not_programmed",
    4: "not_configured",
    5: "attack_counter",
    6: "ursk_decrypt_failure",
}

_TOS_ACCEPTANCE_MAP: Final[dict[int, str]] = {
    1: "not_accepted",
    2: "accepted",
}

_VIDEO_MODE_MAP: Final[dict[int, str]] = {
    0: "none",
    1: "everywhere",
    2: "away_from_home",
}

_VIDEO_MONITORING_STATUS_MAP: Final[dict[int, str]] = {
    1: "disabled",
    2: "enabled",
    3: "active",
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
        "consecutiveAlarmDisabledNotification": _present(
            m, "consecutive_alarm_disabled_notification"
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
