"""Tests for the `user_passcodes.*` decoders."""

from __future__ import annotations

import pytest

from rivian.parallax.proto import user_passcodes_pb2 as user_passcodes

from .helpers import decode


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (user_passcodes.DRIVE_AUTH_ENABLED, True),
        (user_passcodes.DRIVE_AUTH_DISABLED, False),
        (7, 7),  # unrecognized values pass through raw
    ],
)
def test_multi_factor_drive(state: int, expected: bool | int) -> None:
    """The drive-auth state maps to whether multi-factor drive is on."""
    result = decode(
        "user_passcodes.passcode_types.drive_auth",
        user_passcodes.DriveAuthPasscode(state=state),  # type: ignore[arg-type]
    )
    assert result == {"multiFactorDriveEnabled": expected}
