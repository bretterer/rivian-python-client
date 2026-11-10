"""Tests for the `security.*` decoders."""

from __future__ import annotations

from rivian.parallax import encode_live_streaming
from rivian.parallax.proto import security_pb2 as security

from .helpers import decode


def test_passive_entry_debug() -> None:
    """Field 1 is the fail reason; field 2 the lock-fail notification."""
    result = decode(
        "security.access.passive_entry_debug",
        security.PassiveEntryDebug(
            reason=security.PASSIVE_ENTRY_AT_HOME_DISABLE,
            send_lock_fail_notification=security.LOCK_FAIL_NOTIFICATION_FALSE,
        ),
    )
    assert result == {
        "passiveEntryUnlockFailReason": "at_home_disable",
        "passiveEntrySendLockFailNotification": "false",
    }


def test_alarm_state() -> None:
    """Field 1 is the alarm sound status; field 2 the disabled notification."""
    result = decode(
        "security.alarm.state",
        security.AlarmState(
            sound_alarm=security.ALARM_SOUND_FALSE,
            consecutive_alarm_disabled_notification=True,
        ),
    )
    assert result == {
        "alarmSoundStatus": "false",
        "consecutiveAlarmDisabledNotification": True,
    }


def test_encode_live_streaming() -> None:
    """A live stream start names the camera and the viewer's device id."""
    request = security.LiveStreamingRequest.FromString(
        encode_live_streaming("rear", "viewer")
    )
    assert request.camera == security.GEAR_GUARD_CAMERA_REAR
    assert request.device_id == "viewer"
