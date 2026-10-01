"""Decoders for `device_table.*` RVM topics."""

from __future__ import annotations

from typing import Any

from .core import RVMDecoder, _present
from .proto import device_table_pb2


@RVMDecoder.register(
    "device_table.vas_keyper.devices", device_table_pb2.VasKeyperDevices
)
def decode_vas_keyper_devices(m: device_table_pb2.VasKeyperDevices) -> dict[str, Any]:
    """device_table.vas_keyper.devices — a paired key (phone, fob or card).

    Fields (partial updates, so each only when sent):
        mappedIdentityId: str — the GraphQL device's `mappedIdentityId`
        hrid: str — short human-readable id
        pairingId: str
        infoStatus: int — small enum-like value
        infoA, infoB, infoC: int — unknown
        deviceId: str — hex; the GraphQL `devices[].id`
        credentialHex: str — hex; likely key material
        keyType: int — raw enum
        active: bool
    """
    result: dict[str, Any] = {}
    if m.HasField("device"):
        for field, key in (
            ("mapped_identity_id", "mappedIdentityId"),
            ("hrid", "hrid"),
            ("pairing_id", "pairingId"),
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
            ("status", "infoStatus"),
            ("b", "infoB"),
        ):
            if (v := _present(credentials.info, field)) is not None:
                result[key] = v
    if credentials.HasField("ble"):
        if (device_id := _present(credentials.ble, "device_id")) is not None:
            result["deviceId"] = device_id.hex()
        if (cred := _present(credentials.ble, "credential")) is not None:
            result["credentialHex"] = cred.hex()
    if (v := _present(credentials, "key_type")) is not None:
        result["keyType"] = v
    if (v := _present(credentials, "active")) is not None:
        result["active"] = v
    return result
