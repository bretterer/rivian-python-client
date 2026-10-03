"""Tests for the `vehicle_access.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import vehicle_access_pb2 as vehicle_access

from .helpers import decode


def test_passive_entry_state() -> None:
    """Both fields map when sent; an empty payload decodes to nothing."""
    rvm = "vehicle_access.state.passive_entry"
    result = decode(
        rvm,
        vehicle_access.PassiveEntryState(
            allow_bluetooth_while_in_ccc=True,
            ccc_passive_permission=vehicle_access.CCC_PASSIVE_PERMISSION_ENABLED,
        ),
    )
    assert result == {
        "passiveEntryBluetoothInCcc": True,
        "cccPassivePermissionStatus": "enabled",
    }
    assert decode(rvm) == {}
