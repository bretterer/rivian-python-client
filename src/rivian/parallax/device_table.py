"""Decoders for `device_table.*` RVM topics."""

from __future__ import annotations

import uuid
from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import device_table_pb2

_Devices = device_table_pb2.VasKeyperDevices
_KEY_STATUS_MAP: Final[dict[int, str]] = {
    _Devices.KEY_STATUS_ACTIVE: "active",
    _Devices.KEY_STATUS_INACTIVE: "inactive",
    _Devices.KEY_STATUS_WAITING_TO_PAIR: "waiting_to_pair",
    _Devices.KEY_STATUS_PAIRING: "pairing",
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
        mappedIdentityId: str — the GraphQL device's `mappedIdentityId`
        hrid: str — short human-readable id (key card)
        profileId: str — the driver profile the key belongs to (as in
            vehicle.profiles.active_user)
        publicKey: str — hex; phone keys
        keyRevision: int — key table revision when the entry was last written
        vehicleResponseRequired: bool
        keyStatus: str ("active" | "inactive" | "waiting_to_pair" |
            "pairing"); inactive covers unpaired, no longer paired and
            deleted keys
        infoC: int — 1 while active, 2147483647 while inactive, else the
            pairing attempt number
        infoA, infoB: int — unknown
        deviceId: str — hex; for a key card, the GraphQL `devices[].id`
        phoneId: str — the phone's UUID; phone keys
        credentialHex: str — hex; likely key material
        active: bool
    """
    result: dict[str, Any] = {}
    if m.HasField("label"):
        if (v := _present(m.label, "name")) is not None:
            result["deviceName"] = v
        if (v := _present(m.label, "key_type")) is not None:
            result["keyType"] = _enum(_KEY_TYPE_MAP, v, what="key type")
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
    for field in ("card", "fob", "phone"):
        if not credentials.HasField(field):
            continue
        material = getattr(credentials, field)
        if (ident := _present(material, "id")) is not None:
            if field == "phone" and len(ident) == 16:
                result["phoneId"] = str(uuid.UUID(bytes=ident))
            else:
                result["deviceId"] = ident.hex()
        if (cred := _present(material, "credential")) is not None:
            result["credentialHex"] = cred.hex()
    if (v := _present(credentials, "key_type")) is not None:
        result["keyType"] = _enum(_KEY_TYPE_MAP, v, what="key type")
    if (v := _present(credentials, "active")) is not None:
        result["active"] = v
    return result
