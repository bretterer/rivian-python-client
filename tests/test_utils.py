"""Test utils module."""

from __future__ import annotations

import pytest

from rivian import VehicleCommand, utils

PHONE_NONCE = bytes.fromhex("e4e9b1f0abba398bdfe5b2d90cba16ad")
PRIVATE_KEY = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JR0hBZ0VBTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEJHMHdhd0lCQVFRZ0tzMzNEek8rbjBZbVI1RFUKNUFIb2N6cUw1RlBXdUZSZ2E4ano1QVZmbWl5aFJBTkNBQVRIL2lQSmxtbTh5RjdsUFJOYlcvZFFDTDJseVpjWQo4U0dKcGpNQ1k4WkhCa0xXV3hoSTZ6RVFTdW5QaUM0Vy9zYUpPVW5EVm15N1Vkbm1EOCtzOCtFNAotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg=="
VEHICLE_KEY = "04334cc40a88768920b54bdfdcd38238df2ec65ce3605a1d343ef2ab8c1a1daa0545cbb804ebf3ab89826924ea3011352b1d23957a52de0acd5a326078d222d31c"


def test_generate_key_pair() -> None:
    """Test generating an ECDH public-private key pair."""
    public_key, private_key = utils.generate_key_pair()
    assert public_key, private_key


COMMAND_HMAC = bytes.fromhex(
    "935bde3fe77d5501635e16e2a9f2e867038e6a2bd6c5936d0b315ab38e0993dd"
)


def test_generate_command_hmac() -> None:
    """Test generating a command HMAC."""
    hmac = utils.generate_command_hmac(PHONE_NONCE, VEHICLE_KEY, PRIVATE_KEY)
    assert hmac == COMMAND_HMAC


def test_generate_ble_command_hmac_is_deprecated(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the deprecated name warns and still returns the command HMAC."""
    with pytest.warns(DeprecationWarning, match="generate_command_hmac") as record:
        hmac = utils.generate_ble_command_hmac(PHONE_NONCE, VEHICLE_KEY, PRIVATE_KEY)
    assert hmac == COMMAND_HMAC
    # The warning points at the caller, not at the deprecated function
    assert record[0].filename == __file__
    assert "generate_ble_command_hmac has been deprecated" in caplog.text


def test_generate_vehicle_command_hmac() -> None:
    """Test generating a vehicle command HMAC."""
    command = str(VehicleCommand.WAKE_VEHICLE)
    timestamp = "1707000000"
    hmac = utils.generate_vehicle_command_hmac(
        command, timestamp, VEHICLE_KEY, PRIVATE_KEY
    )
    assert hmac == "2a68bdda69ff8643e37bac595905f6a481435e00bb63bdd415ecbb425a5bb598"


def test_place_url() -> None:
    """A place link carries the place's name, id, address and coordinates."""
    assert utils.place_url("place_id", "REI", 41.5, -93.7, "1 Main St") == (
        "https://telenav.id/entity?geo_coordinates=41.5%2C-93.7&entity_id=place_id"
        "&name=REI&nav_coordinates=41.5%2C-93.7&address=1+Main+St&source_type=telenav"
    )
    assert "address" not in utils.place_url("place_id", "REI", 41.5, -93.7)
