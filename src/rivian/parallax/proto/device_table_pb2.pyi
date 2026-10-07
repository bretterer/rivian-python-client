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
    class DeviceOem(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEVICE_OEM_UNKNOWN: _ClassVar[VasKeyperDevices.DeviceOem]
        DEVICE_OEM_RIVIAN: _ClassVar[VasKeyperDevices.DeviceOem]
        DEVICE_OEM_APPLE: _ClassVar[VasKeyperDevices.DeviceOem]
        DEVICE_OEM_GOOGLE: _ClassVar[VasKeyperDevices.DeviceOem]
        DEVICE_OEM_SAMSUNG: _ClassVar[VasKeyperDevices.DeviceOem]
        DEVICE_OEM_VW: _ClassVar[VasKeyperDevices.DeviceOem]
    DEVICE_OEM_UNKNOWN: VasKeyperDevices.DeviceOem
    DEVICE_OEM_RIVIAN: VasKeyperDevices.DeviceOem
    DEVICE_OEM_APPLE: VasKeyperDevices.DeviceOem
    DEVICE_OEM_GOOGLE: VasKeyperDevices.DeviceOem
    DEVICE_OEM_SAMSUNG: VasKeyperDevices.DeviceOem
    DEVICE_OEM_VW: VasKeyperDevices.DeviceOem
    class Label(_message.Message):
        __slots__ = ("name", "key_type", "deletable", "wcc_version")
        NAME_FIELD_NUMBER: _ClassVar[int]
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        DELETABLE_FIELD_NUMBER: _ClassVar[int]
        WCC_VERSION_FIELD_NUMBER: _ClassVar[int]
        name: str
        key_type: VasKeyperDevices.KeyType
        deletable: bool
        wcc_version: int
        def __init__(self, name: _Optional[str] = ..., key_type: _Optional[_Union[VasKeyperDevices.KeyType, str]] = ..., deletable: bool = ..., wcc_version: _Optional[int] = ...) -> None: ...
    class Device(_message.Message):
        __slots__ = ("mapped_identity_id", "hrid", "profile_id", "public_key", "revision", "vehicle_response_required")
        MAPPED_IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
        HRID_FIELD_NUMBER: _ClassVar[int]
        PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
        PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
        REVISION_FIELD_NUMBER: _ClassVar[int]
        VEHICLE_RESPONSE_REQUIRED_FIELD_NUMBER: _ClassVar[int]
        mapped_identity_id: str
        hrid: str
        profile_id: str
        public_key: str
        revision: int
        vehicle_response_required: int
        def __init__(self, mapped_identity_id: _Optional[str] = ..., hrid: _Optional[str] = ..., profile_id: _Optional[str] = ..., public_key: _Optional[str] = ..., revision: _Optional[int] = ..., vehicle_response_required: _Optional[int] = ...) -> None: ...
    class Credentials(_message.Message):
        __slots__ = ("info", "signed_cloud", "owner", "friend", "card", "fob", "phone", "fob2", "key_type", "device_oem")
        class Info(_message.Message):
            __slots__ = ("a", "created_at", "expires_at", "c", "status", "b", "permissions")
            A_FIELD_NUMBER: _ClassVar[int]
            CREATED_AT_FIELD_NUMBER: _ClassVar[int]
            EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
            C_FIELD_NUMBER: _ClassVar[int]
            STATUS_FIELD_NUMBER: _ClassVar[int]
            B_FIELD_NUMBER: _ClassVar[int]
            PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
            a: int
            created_at: int
            expires_at: int
            c: int
            status: VasKeyperDevices.KeyStatus
            b: int
            permissions: int
            def __init__(self, a: _Optional[int] = ..., created_at: _Optional[int] = ..., expires_at: _Optional[int] = ..., c: _Optional[int] = ..., status: _Optional[_Union[VasKeyperDevices.KeyStatus, str]] = ..., b: _Optional[int] = ..., permissions: _Optional[int] = ...) -> None: ...
        class SignedCloud(_message.Message):
            __slots__ = ("payload",)
            PAYLOAD_FIELD_NUMBER: _ClassVar[int]
            payload: str
            def __init__(self, payload: _Optional[str] = ...) -> None: ...
        class OwnerKey(_message.Message):
            __slots__ = ("spake_w0", "spake_l", "salt", "id", "credential")
            SPAKE_W0_FIELD_NUMBER: _ClassVar[int]
            SPAKE_L_FIELD_NUMBER: _ClassVar[int]
            SALT_FIELD_NUMBER: _ClassVar[int]
            ID_FIELD_NUMBER: _ClassVar[int]
            CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
            spake_w0: bytes
            spake_l: bytes
            salt: bytes
            id: bytes
            credential: bytes
            def __init__(self, spake_w0: _Optional[bytes] = ..., spake_l: _Optional[bytes] = ..., salt: _Optional[bytes] = ..., id: _Optional[bytes] = ..., credential: _Optional[bytes] = ...) -> None: ...
        class FriendKey(_message.Message):
            __slots__ = ("id", "credential")
            ID_FIELD_NUMBER: _ClassVar[int]
            CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
            id: bytes
            credential: bytes
            def __init__(self, id: _Optional[bytes] = ..., credential: _Optional[bytes] = ...) -> None: ...
        class DualKey(_message.Message):
            __slots__ = ("ble_id", "ble_credential", "nfc_id", "nfc_credential")
            BLE_ID_FIELD_NUMBER: _ClassVar[int]
            BLE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
            NFC_ID_FIELD_NUMBER: _ClassVar[int]
            NFC_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
            ble_id: bytes
            ble_credential: bytes
            nfc_id: bytes
            nfc_credential: bytes
            def __init__(self, ble_id: _Optional[bytes] = ..., ble_credential: _Optional[bytes] = ..., nfc_id: _Optional[bytes] = ..., nfc_credential: _Optional[bytes] = ...) -> None: ...
        INFO_FIELD_NUMBER: _ClassVar[int]
        SIGNED_CLOUD_FIELD_NUMBER: _ClassVar[int]
        OWNER_FIELD_NUMBER: _ClassVar[int]
        FRIEND_FIELD_NUMBER: _ClassVar[int]
        CARD_FIELD_NUMBER: _ClassVar[int]
        FOB_FIELD_NUMBER: _ClassVar[int]
        PHONE_FIELD_NUMBER: _ClassVar[int]
        FOB2_FIELD_NUMBER: _ClassVar[int]
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        DEVICE_OEM_FIELD_NUMBER: _ClassVar[int]
        info: VasKeyperDevices.Credentials.Info
        signed_cloud: VasKeyperDevices.Credentials.SignedCloud
        owner: VasKeyperDevices.Credentials.OwnerKey
        friend: VasKeyperDevices.Credentials.FriendKey
        card: VasKeyperDevices.KeyMaterial
        fob: VasKeyperDevices.KeyMaterial
        phone: VasKeyperDevices.KeyMaterial
        fob2: VasKeyperDevices.Credentials.DualKey
        key_type: VasKeyperDevices.KeyType
        device_oem: VasKeyperDevices.DeviceOem
        def __init__(self, info: _Optional[_Union[VasKeyperDevices.Credentials.Info, _Mapping]] = ..., signed_cloud: _Optional[_Union[VasKeyperDevices.Credentials.SignedCloud, _Mapping]] = ..., owner: _Optional[_Union[VasKeyperDevices.Credentials.OwnerKey, _Mapping]] = ..., friend: _Optional[_Union[VasKeyperDevices.Credentials.FriendKey, _Mapping]] = ..., card: _Optional[_Union[VasKeyperDevices.KeyMaterial, _Mapping]] = ..., fob: _Optional[_Union[VasKeyperDevices.KeyMaterial, _Mapping]] = ..., phone: _Optional[_Union[VasKeyperDevices.KeyMaterial, _Mapping]] = ..., fob2: _Optional[_Union[VasKeyperDevices.Credentials.DualKey, _Mapping]] = ..., key_type: _Optional[_Union[VasKeyperDevices.KeyType, str]] = ..., device_oem: _Optional[_Union[VasKeyperDevices.DeviceOem, str]] = ...) -> None: ...
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
