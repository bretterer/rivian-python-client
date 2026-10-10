from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConsentValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONSENT_UNKNOWN: _ClassVar[ConsentValue]
    CONSENT_NOT_APPLICABLE: _ClassVar[ConsentValue]
    CONSENT_CONSENTED: _ClassVar[ConsentValue]
    CONSENT_NOT_CONSENTED: _ClassVar[ConsentValue]

class DailyLimitValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DAILY_LIMIT_UNDEFINED: _ClassVar[DailyLimitValue]
    DAILY_LIMIT_HIT: _ClassVar[DailyLimitValue]
    DAILY_LIMIT_NOT_HIT: _ClassVar[DailyLimitValue]
CONSENT_UNKNOWN: ConsentValue
CONSENT_NOT_APPLICABLE: ConsentValue
CONSENT_CONSENTED: ConsentValue
CONSENT_NOT_CONSENTED: ConsentValue
DAILY_LIMIT_UNDEFINED: DailyLimitValue
DAILY_LIMIT_HIT: DailyLimitValue
DAILY_LIMIT_NOT_HIT: DailyLimitValue

class GearGuardStreamingConsent(_message.Message):
    __slots__ = ("consent",)
    CONSENT_FIELD_NUMBER: _ClassVar[int]
    consent: ConsentValue
    def __init__(self, consent: _Optional[_Union[ConsentValue, str]] = ...) -> None: ...

class GearGuardStreamingDailyLimit(_message.Message):
    __slots__ = ("limit", "limit_reset_time")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    LIMIT_RESET_TIME_FIELD_NUMBER: _ClassVar[int]
    limit: DailyLimitValue
    limit_reset_time: int
    def __init__(self, limit: _Optional[_Union[DailyLimitValue, str]] = ..., limit_reset_time: _Optional[int] = ...) -> None: ...
