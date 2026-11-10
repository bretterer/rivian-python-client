"""Utilities."""

from __future__ import annotations

import hashlib
import hmac
import logging
from base64 import b64decode, b64encode
from datetime import UTC, datetime
from typing import cast
from urllib.parse import urlencode
from warnings import warn

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

_LOGGER = logging.getLogger(__name__)


def send_deprecation_warning(old_name: str, new_name: str) -> None:
    """Send a deprecation warning."""
    message = f"{old_name} has been deprecated in favor of {new_name}, the alias will be removed in the future"
    warn(
        message,
        DeprecationWarning,
        # Point at the code that called the deprecated function
        stacklevel=3,
    )
    _LOGGER.warning(message)


def base64_encode(data: bytes) -> str:
    """Encode bytes to Base64 string"""
    return b64encode(data).decode("utf-8")


def decode_private_key(private_key_str: str) -> ec.EllipticCurvePrivateKey:
    """Decode an EC private key."""
    key = serialization.load_pem_private_key(b64decode(private_key_str), password=None)
    return cast(ec.EllipticCurvePrivateKey, key)


def decode_public_key(public_key_str) -> ec.EllipticCurvePublicKey:
    """Decode an EC public key."""
    return ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), bytes.fromhex(public_key_str)
    )


def encode_private_key(private_key: ec.EllipticCurvePrivateKey) -> str:
    """Encode an EC public key."""
    return base64_encode(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )


def encode_public_key(public_key: ec.EllipticCurvePublicKey) -> str:
    """Encode an EC public key."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    ).hex()


def generate_key_pair() -> tuple[str, str]:
    """Generate an ECDH public-private key pair.

    Copied from https://rivian-api.kaedenb.org/app/controls/enroll-phone/
    """
    # Generate a private key
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Get the corresponding public key
    public_key = private_key.public_key()

    # Serialize the keys in the standard format
    private_key_str = encode_private_key(private_key)
    public_key_str = encode_public_key(public_key)

    # Return the public-private key pair as strings
    return (public_key_str, private_key_str)


def generate_command_hmac(data: bytes, vehicle_key: str, private_key: str) -> bytes:
    """Return the raw HMAC-SHA256 of `data`, keyed by the phone and vehicle keys.

    Signs BLE commands and signed Parallax commands alike.
    """
    secret_key = get_secret_key(private_key, vehicle_key)
    return bytes.fromhex(get_message_signature(secret_key, data))


# TODO: Remove around 2027-05, six months after its deprecation in 2026-11
def generate_ble_command_hmac(
    hmac_data: bytes, vehicle_key: str, private_key: str
) -> bytes:
    """Generate ble command hmac.

    Deprecated: use `generate_command_hmac`.
    """
    send_deprecation_warning("generate_ble_command_hmac", "generate_command_hmac")
    return generate_command_hmac(hmac_data, vehicle_key, private_key)


def generate_vehicle_command_hmac(
    command: str, timestamp: str, vehicle_key: str, private_key: str
):
    """Generate vehicle command hmac."""
    message = (command + timestamp).encode("utf-8")
    secret_key = get_secret_key(private_key, vehicle_key)
    return get_message_signature(secret_key, message)


def get_message_signature(secret_key: bytes, message: bytes) -> str:
    """Get message signature."""
    return hmac.new(secret_key, message, hashlib.sha256).hexdigest()


def get_secret_key(private_key_str: str, public_key_str: str) -> bytes:
    """Get HKDF derived secret key from private/public key pair."""
    private_key = decode_private_key(private_key_str)
    public_key = decode_public_key(public_key_str)
    secret = private_key.exchange(ec.ECDH(), public_key)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"")
    return hkdf.derive(secret)


# Anything at or above this magnitude is treated as milliseconds rather
# than seconds. A seconds-scale Unix epoch stays below 1e11 until the
# year 5138; a milliseconds-scale one is already above 1e12 today. 1e11
# sits comfortably in the gap between the two, with room on both sides.
_MS_THRESHOLD = 1e11


def from_epoch(epoch: float) -> datetime:
    """Convert a Unix epoch value in either seconds or milliseconds to a
    timezone-aware UTC `datetime`.
    """
    if abs(epoch) >= _MS_THRESHOLD:
        epoch /= 1000
    return datetime.fromtimestamp(epoch, UTC)


def place_url(
    place_id: str,
    name: str,
    latitude: float,
    longitude: float,
    address: str | None = None,
) -> str:
    """Return the Rivian app's link for a place, for `send_location_to_vehicle`.

    The vehicle shows the place's name. `place_id` is a Google place id, such as a
    `search_places` result's `id`; Rivian refuses these links without one. Use the
    result's `navCoordinate`, where the drive ends.
    """
    coordinates = f"{latitude},{longitude}"
    query = {
        "geo_coordinates": coordinates,
        "entity_id": place_id,
        "name": name,
        "nav_coordinates": coordinates,
        "address": address,
        "source_type": "telenav",
    }
    return "https://telenav.id/entity?" + urlencode(
        {k: v for k, v in query.items() if v is not None}
    )
