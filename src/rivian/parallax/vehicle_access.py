"""Decoders for `vehicle_access.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import vehicle_access_pb2

_CCC_PASSIVE_PERMISSION_MAP: Final[dict[int, str]] = {
    vehicle_access_pb2.CCC_PASSIVE_PERMISSION_SNA: "sna",
    vehicle_access_pb2.CCC_PASSIVE_PERMISSION_DISABLED: "disabled",
    vehicle_access_pb2.CCC_PASSIVE_PERMISSION_ENABLED: "enabled",
}

_CCC_PASSIVE_SETTING_MAP: Final[dict[int, str]] = {
    vehicle_access_pb2.CCC_PASSIVE_SETTING_UNAVAILABLE: "unavailable",
    vehicle_access_pb2.CCC_PASSIVE_SETTING_DISABLED: "disabled",
    vehicle_access_pb2.CCC_PASSIVE_SETTING_ENABLED: "enabled",
}


@RVMDecoder.register(
    "vehicle_access.passive_entry.passive_entry",
    vehicle_access_pb2.PassiveEntrySetting,
)
def decode_passive_entry_setting(
    m: vehicle_access_pb2.PassiveEntrySetting,
) -> dict[str, Any]:
    """vehicle_access.passive_entry.passive_entry — passive entry setting.

    Not seen yet; the schema comes from the app.

    Fields:
        cccPassivePermission: str ("unavailable" | "disabled" | "enabled")
    """
    return {
        "cccPassivePermission": _enum(
            _CCC_PASSIVE_SETTING_MAP,
            m.ccc_passive_permission,
            what="CCC passive setting",
        )
    }


@RVMDecoder.register(
    "vehicle_access.state.passive_entry", vehicle_access_pb2.PassiveEntryState
)
def decode_vehicle_access_passive_entry(
    m: vehicle_access_pb2.PassiveEntryState,
) -> dict[str, Any]:
    """vehicle_access.state.passive_entry — digital-key passive entry state.

    Not seen yet; the schema comes from the app.

    Fields (each only when sent):
        passiveEntryBluetoothInCcc: bool — Bluetooth passive entry allowed
            while using a CCC digital key
        cccPassivePermissionStatus: str ("sna" | "disabled" | "enabled")
    """
    result: dict[str, Any] = {}
    if (v := _present(m, "allow_bluetooth_while_in_ccc")) is not None:
        result["passiveEntryBluetoothInCcc"] = v
    if (v := _present(m, "ccc_passive_permission")) is not None:
        result["cccPassivePermissionStatus"] = _enum(
            _CCC_PASSIVE_PERMISSION_MAP, v, what="CCC passive permission"
        )
    return result
