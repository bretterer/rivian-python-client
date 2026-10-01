from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DriveAuthState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRIVE_AUTH_STATE_UNSPECIFIED: _ClassVar[DriveAuthState]
    DRIVE_AUTH_DISABLED: _ClassVar[DriveAuthState]
    DRIVE_AUTH_ENABLED: _ClassVar[DriveAuthState]
DRIVE_AUTH_STATE_UNSPECIFIED: DriveAuthState
DRIVE_AUTH_DISABLED: DriveAuthState
DRIVE_AUTH_ENABLED: DriveAuthState

class DriveAuthPasscode(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: DriveAuthState
    def __init__(self, state: _Optional[_Union[DriveAuthState, str]] = ...) -> None: ...
