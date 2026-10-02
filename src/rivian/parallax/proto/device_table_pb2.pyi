from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VasKeyperDevices(_message.Message):
    __slots__ = ("field_1", "device", "credentials")
    class Unmapped1(_message.Message):
        __slots__ = ("field_3",)
        FIELD_3_FIELD_NUMBER: _ClassVar[int]
        field_3: int
        def __init__(self, field_3: _Optional[int] = ...) -> None: ...
    class Device(_message.Message):
        __slots__ = ("mapped_identity_id", "hrid", "pairing_id", "field_5")
        MAPPED_IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
        HRID_FIELD_NUMBER: _ClassVar[int]
        PAIRING_ID_FIELD_NUMBER: _ClassVar[int]
        FIELD_5_FIELD_NUMBER: _ClassVar[int]
        mapped_identity_id: str
        hrid: str
        pairing_id: str
        field_5: int
        def __init__(self, mapped_identity_id: _Optional[str] = ..., hrid: _Optional[str] = ..., pairing_id: _Optional[str] = ..., field_5: _Optional[int] = ...) -> None: ...
    class Credentials(_message.Message):
        __slots__ = ("info", "ble", "key_type", "active")
        class Info(_message.Message):
            __slots__ = ("a", "c", "status", "b")
            A_FIELD_NUMBER: _ClassVar[int]
            C_FIELD_NUMBER: _ClassVar[int]
            STATUS_FIELD_NUMBER: _ClassVar[int]
            B_FIELD_NUMBER: _ClassVar[int]
            a: int
            c: int
            status: int
            b: int
            def __init__(self, a: _Optional[int] = ..., c: _Optional[int] = ..., status: _Optional[int] = ..., b: _Optional[int] = ...) -> None: ...
        class Ble(_message.Message):
            __slots__ = ("device_id", "credential")
            DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
            CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
            device_id: bytes
            credential: bytes
            def __init__(self, device_id: _Optional[bytes] = ..., credential: _Optional[bytes] = ...) -> None: ...
        INFO_FIELD_NUMBER: _ClassVar[int]
        BLE_FIELD_NUMBER: _ClassVar[int]
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        info: VasKeyperDevices.Credentials.Info
        ble: VasKeyperDevices.Credentials.Ble
        key_type: int
        active: bool
        def __init__(self, info: _Optional[_Union[VasKeyperDevices.Credentials.Info, _Mapping]] = ..., ble: _Optional[_Union[VasKeyperDevices.Credentials.Ble, _Mapping]] = ..., key_type: _Optional[int] = ..., active: _Optional[bool] = ...) -> None: ...
    FIELD_1_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    field_1: VasKeyperDevices.Unmapped1
    device: VasKeyperDevices.Device
    credentials: VasKeyperDevices.Credentials
    def __init__(self, field_1: _Optional[_Union[VasKeyperDevices.Unmapped1, _Mapping]] = ..., device: _Optional[_Union[VasKeyperDevices.Device, _Mapping]] = ..., credentials: _Optional[_Union[VasKeyperDevices.Credentials, _Mapping]] = ...) -> None: ...
