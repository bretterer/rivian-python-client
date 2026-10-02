from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HardwareFailure(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HARDWARE_FAILURE_UNSPECIFIED: _ClassVar[HardwareFailure]
    HARDWARE_FAILURE_SET: _ClassVar[HardwareFailure]

class ImmobilizerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMMOBILIZER_NOT_ASSIGNED: _ClassVar[ImmobilizerStatus]
    IMMOBILIZER_NOT_AUTHORIZED: _ClassVar[ImmobilizerStatus]
    IMMOBILIZER_AUTHORIZED_TO_DRIVE: _ClassVar[ImmobilizerStatus]

class PassiveEntryFailReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PASSIVE_ENTRY_FAIL_UNSPECIFIED: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_NOT_IN_PARK: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_AT_HOME_DISABLE: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_PASSENGER_IN_SEAT: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_DEVICE_NOT_ENABLED: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_TRANSPORT_MODE: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_CAR_WASH_MODE: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_CAMP_MODE: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_ACTIVE_OTA: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_SHOW_AND_TELL_MODE: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_RCVD_RSSI_PENDING: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_LOCK_ONLY_AT_HOME: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_CAR_COSTUME_MODE: _ClassVar[PassiveEntryFailReason]
    PASSIVE_ENTRY_SLEPT_IMMEDIATE: _ClassVar[PassiveEntryFailReason]

class SecureElementFaulted(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SECURE_ELEMENT_FAULT_UNSPECIFIED: _ClassVar[SecureElementFaulted]
    SECURE_ELEMENT_NO_FAILURE: _ClassVar[SecureElementFaulted]
    SECURE_ELEMENT_LOST_COMMUNICATION: _ClassVar[SecureElementFaulted]
    SECURE_ELEMENT_APPLET_NOT_PROGRAMMED: _ClassVar[SecureElementFaulted]
    SECURE_ELEMENT_NOT_CONFIGURED: _ClassVar[SecureElementFaulted]
    SECURE_ELEMENT_ATTACK_COUNTER: _ClassVar[SecureElementFaulted]
    SECURE_ELEMENT_URSK_DECRYPT_FAILURE: _ClassVar[SecureElementFaulted]

class AccessCanFaulted(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACCESS_CAN_FAULT_UNSPECIFIED: _ClassVar[AccessCanFaulted]
    ACCESS_CAN_NO_FAILURE: _ClassVar[AccessCanFaulted]
    ACCESS_CAN_FAILURE: _ClassVar[AccessCanFaulted]

class AlarmSound(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALARM_SOUND_UNSPECIFIED: _ClassVar[AlarmSound]
    ALARM_SOUND_FALSE: _ClassVar[AlarmSound]
    ALARM_SOUND_TRUE: _ClassVar[AlarmSound]
    ALARM_SOUND_SIGNAL_NOT_AVAILABLE: _ClassVar[AlarmSound]

class VideoMonitoringStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VIDEO_MONITORING_STATUS_UNSPECIFIED: _ClassVar[VideoMonitoringStatus]
    VIDEO_MONITORING_DISABLED: _ClassVar[VideoMonitoringStatus]
    VIDEO_MONITORING_ENABLED: _ClassVar[VideoMonitoringStatus]
    VIDEO_MONITORING_ACTIVE: _ClassVar[VideoMonitoringStatus]

class VideoMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VIDEO_MODE_NONE: _ClassVar[VideoMode]
    VIDEO_MODE_EVERYWHERE: _ClassVar[VideoMode]
    VIDEO_MODE_AWAY_FROM_HOME: _ClassVar[VideoMode]

class TosAcceptance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOS_ACCEPTANCE_UNSPECIFIED: _ClassVar[TosAcceptance]
    TOS_NOT_ACCEPTED: _ClassVar[TosAcceptance]
    TOS_ACCEPTED: _ClassVar[TosAcceptance]
HARDWARE_FAILURE_UNSPECIFIED: HardwareFailure
HARDWARE_FAILURE_SET: HardwareFailure
IMMOBILIZER_NOT_ASSIGNED: ImmobilizerStatus
IMMOBILIZER_NOT_AUTHORIZED: ImmobilizerStatus
IMMOBILIZER_AUTHORIZED_TO_DRIVE: ImmobilizerStatus
PASSIVE_ENTRY_FAIL_UNSPECIFIED: PassiveEntryFailReason
PASSIVE_ENTRY_NOT_IN_PARK: PassiveEntryFailReason
PASSIVE_ENTRY_AT_HOME_DISABLE: PassiveEntryFailReason
PASSIVE_ENTRY_PASSENGER_IN_SEAT: PassiveEntryFailReason
PASSIVE_ENTRY_DEVICE_NOT_ENABLED: PassiveEntryFailReason
PASSIVE_ENTRY_TRANSPORT_MODE: PassiveEntryFailReason
PASSIVE_ENTRY_CAR_WASH_MODE: PassiveEntryFailReason
PASSIVE_ENTRY_CAMP_MODE: PassiveEntryFailReason
PASSIVE_ENTRY_ACTIVE_OTA: PassiveEntryFailReason
PASSIVE_ENTRY_SHOW_AND_TELL_MODE: PassiveEntryFailReason
PASSIVE_ENTRY_RCVD_RSSI_PENDING: PassiveEntryFailReason
PASSIVE_ENTRY_LOCK_ONLY_AT_HOME: PassiveEntryFailReason
PASSIVE_ENTRY_CAR_COSTUME_MODE: PassiveEntryFailReason
PASSIVE_ENTRY_SLEPT_IMMEDIATE: PassiveEntryFailReason
SECURE_ELEMENT_FAULT_UNSPECIFIED: SecureElementFaulted
SECURE_ELEMENT_NO_FAILURE: SecureElementFaulted
SECURE_ELEMENT_LOST_COMMUNICATION: SecureElementFaulted
SECURE_ELEMENT_APPLET_NOT_PROGRAMMED: SecureElementFaulted
SECURE_ELEMENT_NOT_CONFIGURED: SecureElementFaulted
SECURE_ELEMENT_ATTACK_COUNTER: SecureElementFaulted
SECURE_ELEMENT_URSK_DECRYPT_FAILURE: SecureElementFaulted
ACCESS_CAN_FAULT_UNSPECIFIED: AccessCanFaulted
ACCESS_CAN_NO_FAILURE: AccessCanFaulted
ACCESS_CAN_FAILURE: AccessCanFaulted
ALARM_SOUND_UNSPECIFIED: AlarmSound
ALARM_SOUND_FALSE: AlarmSound
ALARM_SOUND_TRUE: AlarmSound
ALARM_SOUND_SIGNAL_NOT_AVAILABLE: AlarmSound
VIDEO_MONITORING_STATUS_UNSPECIFIED: VideoMonitoringStatus
VIDEO_MONITORING_DISABLED: VideoMonitoringStatus
VIDEO_MONITORING_ENABLED: VideoMonitoringStatus
VIDEO_MONITORING_ACTIVE: VideoMonitoringStatus
VIDEO_MODE_NONE: VideoMode
VIDEO_MODE_EVERYWHERE: VideoMode
VIDEO_MODE_AWAY_FROM_HOME: VideoMode
TOS_ACCEPTANCE_UNSPECIFIED: TosAcceptance
TOS_NOT_ACCEPTED: TosAcceptance
TOS_ACCEPTED: TosAcceptance

class PassiveEntry(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Btm(_message.Message):
    __slots__ = ("ff", "ic", "lfd", "rf", "rfd", "oc")
    FF_FIELD_NUMBER: _ClassVar[int]
    IC_FIELD_NUMBER: _ClassVar[int]
    LFD_FIELD_NUMBER: _ClassVar[int]
    RF_FIELD_NUMBER: _ClassVar[int]
    RFD_FIELD_NUMBER: _ClassVar[int]
    OC_FIELD_NUMBER: _ClassVar[int]
    ff: HardwareFailure
    ic: HardwareFailure
    lfd: HardwareFailure
    rf: HardwareFailure
    rfd: HardwareFailure
    oc: HardwareFailure
    def __init__(self, ff: _Optional[_Union[HardwareFailure, str]] = ..., ic: _Optional[_Union[HardwareFailure, str]] = ..., lfd: _Optional[_Union[HardwareFailure, str]] = ..., rf: _Optional[_Union[HardwareFailure, str]] = ..., rfd: _Optional[_Union[HardwareFailure, str]] = ..., oc: _Optional[_Union[HardwareFailure, str]] = ...) -> None: ...

class ImmobilizerState(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ImmobilizerStatus
    def __init__(self, status: _Optional[_Union[ImmobilizerStatus, str]] = ...) -> None: ...

class PassiveEntryDebug(_message.Message):
    __slots__ = ("reason",)
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: PassiveEntryFailReason
    def __init__(self, reason: _Optional[_Union[PassiveEntryFailReason, str]] = ...) -> None: ...

class VasFault(_message.Message):
    __slots__ = ("secure_element", "access_can")
    SECURE_ELEMENT_FIELD_NUMBER: _ClassVar[int]
    ACCESS_CAN_FIELD_NUMBER: _ClassVar[int]
    secure_element: SecureElementFaulted
    access_can: AccessCanFaulted
    def __init__(self, secure_element: _Optional[_Union[SecureElementFaulted, str]] = ..., access_can: _Optional[_Union[AccessCanFaulted, str]] = ...) -> None: ...

class AlarmState(_message.Message):
    __slots__ = ("consecutive_alarm_disabled_notification", "sound_status")
    CONSECUTIVE_ALARM_DISABLED_NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    SOUND_STATUS_FIELD_NUMBER: _ClassVar[int]
    consecutive_alarm_disabled_notification: int
    sound_status: AlarmSound
    def __init__(self, consecutive_alarm_disabled_notification: _Optional[int] = ..., sound_status: _Optional[_Union[AlarmSound, str]] = ...) -> None: ...

class VideoMonitoringState(_message.Message):
    __slots__ = ("status", "mode", "terms_accepted")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    TERMS_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    status: VideoMonitoringStatus
    mode: VideoMode
    terms_accepted: TosAcceptance
    def __init__(self, status: _Optional[_Union[VideoMonitoringStatus, str]] = ..., mode: _Optional[_Union[VideoMode, str]] = ..., terms_accepted: _Optional[_Union[TosAcceptance, str]] = ...) -> None: ...
