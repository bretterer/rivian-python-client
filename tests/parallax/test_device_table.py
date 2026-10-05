"""Tests for the `device_table.*` decoders."""

from __future__ import annotations

import uuid

from rivian.parallax.proto import device_table_pb2 as device_table

from .helpers import decode

RVM = "device_table.vas_keyper.devices"
Devices = device_table.VasKeyperDevices


def test_phone_key() -> None:
    """A phone key: its name, profile, public key and phone UUID."""
    phone_id = uuid.UUID("12345678-1234-4234-8234-123456789abc")
    result = decode(
        RVM,
        Devices(
            label=Devices.Label(name="My Phone", key_type=Devices.KEY_TYPE_PHONE),
            device=Devices.Device(
                mapped_identity_id="17-id",
                profile_id="02-profile",
                public_key="ab",
                revision=301,
                vehicle_response_required=True,
            ),
            credentials=Devices.Credentials(
                info=Devices.Credentials.Info(
                    a=5, c=2, status=Devices.KEY_STATUS_PAIRING, b=5
                ),
                phone=Devices.KeyMaterial(id=phone_id.bytes, credential=b"\x01\x02"),
                key_type=Devices.KEY_TYPE_PHONE,
            ),
        ),
    )
    assert result == {
        "deviceName": "My Phone",
        "keyType": "phone",
        "mappedIdentityId": "17-id",
        "profileId": "02-profile",
        "publicKey": "ab",
        "keyRevision": 301,
        "vehicleResponseRequired": True,
        "infoA": 5,
        "infoC": 2,
        "infoB": 5,
        "keyStatus": "pairing",
        "phoneId": str(phone_id),
        "credentialHex": "0102",
    }


def test_key_card() -> None:
    """A key card: its short id and device id as hex."""
    result = decode(
        RVM,
        Devices(
            device=Devices.Device(hrid="AB1234"),
            credentials=Devices.Credentials(
                card=Devices.KeyMaterial(id=b"\x0a\x0b", credential=b"\xff"),
                key_type=Devices.KEY_TYPE_KEY_CARD,
                active=True,
            ),
        ),
    )
    assert result == {
        "hrid": "AB1234",
        "deviceId": "0a0b",
        "credentialHex": "ff",
        "keyType": "key_card",
        "active": True,
    }


def test_partial_update() -> None:
    """A status-only update decodes to just that field."""
    result = decode(
        RVM,
        Devices(
            credentials=Devices.Credentials(
                info=Devices.Credentials.Info(status=Devices.KEY_STATUS_INACTIVE)
            )
        ),
    )
    assert result == {"keyStatus": "inactive"}
