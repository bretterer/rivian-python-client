"""Decoders for `user_passcodes.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import _LOGGER, RVMDecoder
from .proto import user_passcodes_pb2

_DRIVE_AUTH_ENABLED: Final[dict[int, bool]] = {
    user_passcodes_pb2.DRIVE_AUTH_DISABLED: False,
    user_passcodes_pb2.DRIVE_AUTH_ENABLED: True,
}


@RVMDecoder.register(
    "user_passcodes.passcode_types.drive_auth", user_passcodes_pb2.DriveAuthPasscode
)
def decode_drive_auth_passcode(
    m: user_passcodes_pb2.DriveAuthPasscode,
) -> dict[str, Any]:
    """user_passcodes.passcode_types.drive_auth — multi-factor drive setting.

    Fields:
        multiFactorDriveEnabled: bool — whether a passcode is needed to drive
    """
    if not m.HasField("state"):
        return {}
    enabled = _DRIVE_AUTH_ENABLED.get(m.state, m.state)
    if not isinstance(enabled, bool):
        _LOGGER.debug("Unknown drive auth state value: %s", m.state)
    return {"multiFactorDriveEnabled": enabled}
