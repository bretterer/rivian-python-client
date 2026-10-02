"""Decoders for `secure_file_transfer.*` RVM topics."""

from __future__ import annotations

from typing import Any

from .core import RVMDecoder
from .proto import secure_file_transfer_pb2


@RVMDecoder.register(
    "secure_file_transfer.pet_snapshot.secure_file",
    secure_file_transfer_pb2.PetSnapshotSecureFile,
)
def decode_pet_snapshot_secure_file(
    _m: secure_file_transfer_pb2.PetSnapshotSecureFile,
) -> dict[str, Any]:
    """secure_file_transfer.pet_snapshot.secure_file — unmapped."""
    return {}
