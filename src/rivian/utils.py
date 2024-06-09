"""Utilities."""

from __future__ import annotations

import hashlib
import hmac
from base64 import b64decode, b64encode
from typing import cast

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


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


def generate_ble_command_hmac(
    hmac_data: bytes, vehicle_key: str, private_key: str
) -> bytes:
    """Generate ble command hmac."""
    secret_key = get_secret_key(private_key, vehicle_key)
    return bytes.fromhex(get_message_signature(secret_key, hmac_data))


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
