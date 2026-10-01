from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Heartbeat(_message.Message):
    __slots__ = ("field_1", "time", "field_3")
    class Timestamp(_message.Message):
        __slots__ = ("seconds", "nanos")
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        NANOS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        nanos: int
        def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
    FIELD_1_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    field_1: int
    time: Heartbeat.Timestamp
    field_3: Heartbeat.Timestamp
    def __init__(self, field_1: _Optional[int] = ..., time: _Optional[_Union[Heartbeat.Timestamp, _Mapping]] = ..., field_3: _Optional[_Union[Heartbeat.Timestamp, _Mapping]] = ...) -> None: ...
