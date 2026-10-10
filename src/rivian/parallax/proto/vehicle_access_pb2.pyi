from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CccPassiveSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CCC_PASSIVE_SETTING_UNAVAILABLE: _ClassVar[CccPassiveSetting]
    CCC_PASSIVE_SETTING_DISABLED: _ClassVar[CccPassiveSetting]
    CCC_PASSIVE_SETTING_ENABLED: _ClassVar[CccPassiveSetting]

class CccPassivePermission(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CCC_PASSIVE_PERMISSION_SNA: _ClassVar[CccPassivePermission]
    CCC_PASSIVE_PERMISSION_DISABLED: _ClassVar[CccPassivePermission]
    CCC_PASSIVE_PERMISSION_ENABLED: _ClassVar[CccPassivePermission]
CCC_PASSIVE_SETTING_UNAVAILABLE: CccPassiveSetting
CCC_PASSIVE_SETTING_DISABLED: CccPassiveSetting
CCC_PASSIVE_SETTING_ENABLED: CccPassiveSetting
CCC_PASSIVE_PERMISSION_SNA: CccPassivePermission
CCC_PASSIVE_PERMISSION_DISABLED: CccPassivePermission
CCC_PASSIVE_PERMISSION_ENABLED: CccPassivePermission

class PassiveEntrySetting(_message.Message):
    __slots__ = ("ccc_passive_permission",)
    CCC_PASSIVE_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    ccc_passive_permission: CccPassiveSetting
    def __init__(self, ccc_passive_permission: _Optional[_Union[CccPassiveSetting, str]] = ...) -> None: ...

class PassiveEntryState(_message.Message):
    __slots__ = ("allow_bluetooth_while_in_ccc", "ccc_passive_permission")
    ALLOW_BLUETOOTH_WHILE_IN_CCC_FIELD_NUMBER: _ClassVar[int]
    CCC_PASSIVE_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    allow_bluetooth_while_in_ccc: bool
    ccc_passive_permission: CccPassivePermission
    def __init__(self, allow_bluetooth_while_in_ccc: bool = ..., ccc_passive_permission: _Optional[_Union[CccPassivePermission, str]] = ...) -> None: ...
