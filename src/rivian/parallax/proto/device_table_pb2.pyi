from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VasKeyperDevices(_message.Message):
    __slots__ = ("label", "device", "credentials")
    class KeyStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KEY_STATUS_UNSPECIFIED: _ClassVar[VasKeyperDevices.KeyStatus]
        KEY_STATUS_ACTIVE: _ClassVar[VasKeyperDevices.KeyStatus]
        KEY_STATUS_INACTIVE: _ClassVar[VasKeyperDevices.KeyStatus]
        KEY_STATUS_WAITING_TO_PAIR: _ClassVar[VasKeyperDevices.KeyStatus]
        KEY_STATUS_PAIRING: _ClassVar[VasKeyperDevices.KeyStatus]
    KEY_STATUS_UNSPECIFIED: VasKeyperDevices.KeyStatus
    KEY_STATUS_ACTIVE: VasKeyperDevices.KeyStatus
    KEY_STATUS_INACTIVE: VasKeyperDevices.KeyStatus
    KEY_STATUS_WAITING_TO_PAIR: VasKeyperDevices.KeyStatus
    KEY_STATUS_PAIRING: VasKeyperDevices.KeyStatus
    class KeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KEY_TYPE_UNSPECIFIED: _ClassVar[VasKeyperDevices.KeyType]
        KEY_TYPE_PHONE: _ClassVar[VasKeyperDevices.KeyType]
        KEY_TYPE_KEY_CARD: _ClassVar[VasKeyperDevices.KeyType]
        KEY_TYPE_KEY_FOB: _ClassVar[VasKeyperDevices.KeyType]
    KEY_TYPE_UNSPECIFIED: VasKeyperDevices.KeyType
    KEY_TYPE_PHONE: VasKeyperDevices.KeyType
    KEY_TYPE_KEY_CARD: VasKeyperDevices.KeyType
    KEY_TYPE_KEY_FOB: VasKeyperDevices.KeyType
    class Label(_message.Message):
        __slots__ = ("name", "key_type")
        NAME_FIELD_NUMBER: _ClassVar[int]
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        name: str
        key_type: VasKeyperDevices.KeyType
        def __init__(self, name: _Optional[str] = ..., key_type: _Optional[_Union[VasKeyperDevices.KeyType, str]] = ...) -> None: ...
    class Device(_message.Message):
        __slots__ = ("mapped_identity_id", "hrid", "profile_id", "public_key", "revision")
        MAPPED_IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
        HRID_FIELD_NUMBER: _ClassVar[int]
        PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
        PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
        REVISION_FIELD_NUMBER: _ClassVar[int]
        mapped_identity_id: str
        hrid: str
        profile_id: str
        public_key: str
        revision: int
        def __init__(self, mapped_identity_id: _Optional[str] = ..., hrid: _Optional[str] = ..., profile_id: _Optional[str] = ..., public_key: _Optional[str] = ..., revision: _Optional[int] = ...) -> None: ...
    class Credentials(_message.Message):
        __slots__ = ("info", "card", "fob", "phone", "key_type", "active")
        class Info(_message.Message):
            __slots__ = ("a", "c", "status", "b")
            A_FIELD_NUMBER: _ClassVar[int]
            C_FIELD_NUMBER: _ClassVar[int]
            STATUS_FIELD_NUMBER: _ClassVar[int]
            B_FIELD_NUMBER: _ClassVar[int]
            a: int
            c: int
            status: VasKeyperDevices.KeyStatus
            b: int
            def __init__(self, a: _Optional[int] = ..., c: _Optional[int] = ..., status: _Optional[_Union[VasKeyperDevices.KeyStatus, str]] = ..., b: _Optional[int] = ...) -> None: ...
        INFO_FIELD_NUMBER: _ClassVar[int]
        CARD_FIELD_NUMBER: _ClassVar[int]
        FOB_FIELD_NUMBER: _ClassVar[int]
        PHONE_FIELD_NUMBER: _ClassVar[int]
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        info: VasKeyperDevices.Credentials.Info
        card: VasKeyperDevices.KeyMaterial
        fob: VasKeyperDevices.KeyMaterial
        phone: VasKeyperDevices.KeyMaterial
        key_type: VasKeyperDevices.KeyType
        active: bool
        def __init__(self, info: _Optional[_Union[VasKeyperDevices.Credentials.Info, _Mapping]] = ..., card: _Optional[_Union[VasKeyperDevices.KeyMaterial, _Mapping]] = ..., fob: _Optional[_Union[VasKeyperDevices.KeyMaterial, _Mapping]] = ..., phone: _Optional[_Union[VasKeyperDevices.KeyMaterial, _Mapping]] = ..., key_type: _Optional[_Union[VasKeyperDevices.KeyType, str]] = ..., active: bool = ...) -> None: ...
    class KeyMaterial(_message.Message):
        __slots__ = ("id", "credential")
        ID_FIELD_NUMBER: _ClassVar[int]
        CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
        id: bytes
        credential: bytes
        def __init__(self, id: _Optional[bytes] = ..., credential: _Optional[bytes] = ...) -> None: ...
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    label: VasKeyperDevices.Label
    device: VasKeyperDevices.Device
    credentials: VasKeyperDevices.Credentials
    def __init__(self, label: _Optional[_Union[VasKeyperDevices.Label, _Mapping]] = ..., device: _Optional[_Union[VasKeyperDevices.Device, _Mapping]] = ..., credentials: _Optional[_Union[VasKeyperDevices.Credentials, _Mapping]] = ...) -> None: ...
