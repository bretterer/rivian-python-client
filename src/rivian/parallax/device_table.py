"""Decoders for `device_table.*` RVM topics."""

from __future__ import annotations

import uuid
from typing import Any, Final

from ..utils import from_epoch
from .core import RVMDecoder, _enum, _present
from .proto import device_table_pb2

_Devices = device_table_pb2.VasKeyperDevices
_KEY_STATUS_MAP: Final[dict[int, str]] = {
    _Devices.KEY_STATUS_ACTIVE: "active",
    _Devices.KEY_STATUS_INACTIVE: "inactive",
    _Devices.KEY_STATUS_WAITING_TO_PAIR: "waiting_to_pair",
    _Devices.KEY_STATUS_PAIRING: "pairing",
}

_DEVICE_OEM_MAP: Final[dict[int, str]] = {
    _Devices.DEVICE_OEM_UNKNOWN: "unknown",
    _Devices.DEVICE_OEM_RIVIAN: "rivian",
    _Devices.DEVICE_OEM_APPLE: "apple",
    _Devices.DEVICE_OEM_GOOGLE: "google",
    _Devices.DEVICE_OEM_SAMSUNG: "samsung",
    _Devices.DEVICE_OEM_VW: "vw",
}

_KEY_TYPE_MAP: Final[dict[int, str]] = {
    _Devices.KEY_TYPE_PHONE: "phone",
    _Devices.KEY_TYPE_KEY_CARD: "key_card",
    _Devices.KEY_TYPE_KEY_FOB: "key_fob",
}


@RVMDecoder.register(
    "device_table.vas_keyper.devices", device_table_pb2.VasKeyperDevices
)
def decode_vas_keyper_devices(m: device_table_pb2.VasKeyperDevices) -> dict[str, Any]:
    """device_table.vas_keyper.devices — a key (phone, key card or fob).

    Covers every driver's keys. A deleted key isn't removed; it's resent
    as inactive.

    Fields (partial updates, so each only when sent):
        deviceName: str — phone keys, e.g. the phone's name
        keyType: str ("phone" | "key_card" | "key_fob"; key_fob inferred)
        keyDeletable: bool
        wccVersion: int
        mappedIdentityId: str — the GraphQL device's `mappedIdentityId`
        hrid: str — short human-readable id (key card)
        profileId: str — the driver profile the key belongs to (as in
            vehicle.profiles.active_user)
        publicKey: str — hex; phone keys
        keyRevision: int — key table revision when the entry was last written
        vehicleResponseRequired: int — raw
        keyStatus: str ("active" | "inactive" | "waiting_to_pair" |
            "pairing"); inactive covers unpaired, no longer paired and
            deleted keys
        infoC: int — 1 while active, 2147483647 while inactive, else the
            pairing attempt number
        infoA, infoB: int — unknown
        keyPermissions: int — raw
        keyCreatedAt, keyExpiresAt: datetime — when sent and non-zero
        keyMaterial: str — which key material is set ("owner" | "friend" |
            "card" | "fob" | "phone" | "fob2")
        deviceId: str — hex; for a key card, the GraphQL `devices[].id`
        nfcDeviceId: str — hex; fob2's NFC id (deviceId is its BLE id)
        phoneId: str — the phone's UUID; phone keys
        credentialHex: str — hex; the wrapped shared secret
        deviceOem: str ("unknown" | "rivian" | "apple" | "google" |
            "samsung" | "vw") — the device maker
    """
    result: dict[str, Any] = {}
    if m.HasField("label"):
        if (v := _present(m.label, "name")) is not None:
            result["deviceName"] = v
        if (v := _present(m.label, "key_type")) is not None:
            result["keyType"] = _enum(_KEY_TYPE_MAP, v, what="key type")
        if (v := _present(m.label, "deletable")) is not None:
            result["keyDeletable"] = v
        if (v := _present(m.label, "wcc_version")) is not None:
            result["wccVersion"] = v
    if m.HasField("device"):
        for field, key in (
            ("mapped_identity_id", "mappedIdentityId"),
            ("hrid", "hrid"),
            ("profile_id", "profileId"),
            ("public_key", "publicKey"),
            ("revision", "keyRevision"),
            ("vehicle_response_required", "vehicleResponseRequired"),
        ):
            if (v := _present(m.device, field)) is not None:
                result[key] = v

    if not m.HasField("credentials"):
        return result
    credentials = m.credentials
    if credentials.HasField("info"):
        for field, key in (
            ("a", "infoA"),
            ("c", "infoC"),
            ("b", "infoB"),
        ):
            if (v := _present(credentials.info, field)) is not None:
                result[key] = v
        if (v := _present(credentials.info, "status")) is not None:
            result["keyStatus"] = _enum(_KEY_STATUS_MAP, v, what="key status")
        if (v := _present(credentials.info, "permissions")) is not None:
            result["keyPermissions"] = v
        for field, key in (
            ("created_at", "keyCreatedAt"),
            ("expires_at", "keyExpiresAt"),
        ):
            if v := _present(credentials.info, field):
                result[key] = from_epoch(v)
    if (field := credentials.WhichOneof("material")) is not None:
        result["keyMaterial"] = field
        material = getattr(credentials, field)
        id_field, cred_field = (
            ("ble_id", "ble_credential") if field == "fob2" else ("id", "credential")
        )
        if (ident := _present(material, id_field)) is not None:
            if field == "phone" and len(ident) == 16:
                result["phoneId"] = str(uuid.UUID(bytes=ident))
            else:
                result["deviceId"] = ident.hex()
        if (cred := _present(material, cred_field)) is not None:
            result["credentialHex"] = cred.hex()
        if field == "fob2" and (ident := _present(material, "nfc_id")) is not None:
            result["nfcDeviceId"] = ident.hex()
    if (v := _present(credentials, "key_type")) is not None:
        result["keyType"] = _enum(_KEY_TYPE_MAP, v, what="key type")
    if (v := _present(credentials, "device_oem")) is not None:
        result["deviceOem"] = _enum(_DEVICE_OEM_MAP, v, what="device OEM")
    return result
