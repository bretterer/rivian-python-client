"""Decoders for `vehicle.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import vehicle_pb2

_POWER_STATE_MAP: Final[dict[int, str]] = {
    1: "sleep",
    2: "standby",
    3: "ready",
    4: "go",
}


@RVMDecoder.register("vehicle.profiles.active_user", vehicle_pb2.ActiveUserProfile)
def decode_active_user_profile(m: vehicle_pb2.ActiveUserProfile) -> dict[str, Any]:
    """vehicle.profiles.active_user — the active profile.

    Fields:
        activeUserProfileId: str — may be a device or session id rather
            than a driver profile
    """
    if (v := _present(m, "active_user_profile_id")) is None:
        return {}
    return {"activeUserProfileId": v}


@RVMDecoder.register("vehicle.power.state", vehicle_pb2.PowerState)
def decode_power_state(m: vehicle_pb2.PowerState) -> dict[str, Any]:
    """vehicle.power.state — vehicle power state.

    Fields:
        powerState: str ("sleep" | "standby" | "ready" | "go")
    """
    if (v := _present(m, "state")) is None:
        return {}
    return {
        "powerState": _enum(
            _POWER_STATE_MAP, v, what="power state", unmapped_default="standby"
        )
    }


@RVMDecoder.register("vehicle.wheels.vehicle_wheels", vehicle_pb2.VehicleWheels)
def decode_wheels(m: vehicle_pb2.VehicleWheels) -> dict[str, Any]:
    """vehicle.wheels.vehicle_wheels — wheel sets and tire rotation data.

    Fields:
        wheels: list[dict] — wheelPackage, tireOdometer,
            odometerAtLastRotation, rotationReminderInterval, isInstalled,
            tires, currentOdometer (distances in meters)
        wheelsInstalled: int — how many are installed
    """
    wheels = [
        {
            "wheelPackage": w.wheel_package,
            "tireOdometer": w.tire_odometer,
            "odometerAtLastRotation": w.odometer_at_last_rotation,
            "rotationReminderInterval": w.rotation_reminder_interval,
            "isInstalled": w.is_installed,
            "tires": w.tires,
            "currentOdometer": w.current_odometer,
        }
        for w in m.wheel
    ]
    if not wheels:
        return {}
    return {
        "wheels": wheels,
        "wheelsInstalled": sum(1 for w in wheels if w["isInstalled"]),
    }


_CONNECTIVITY_LEVEL_MAP: Final[dict[int, str]] = {
    1: "level_0",
    2: "level_1",
    3: "level_2",
    4: "level_3",
    5: "level_4",
}

_WIFI_SECURITY_MAP: Final[dict[int, str]] = {
    1: "open",
    2: "wpa_personal",
    3: "wpa_enterprise",
    4: "wpa2_personal",
    5: "wpa2_enterprise",
}

_WPA_STATUS_MAP: Final[dict[int, str]] = {
    1: "not_connected",
    2: "connected",
    3: "scanning",
    4: "connecting",
    5: "disconnecting",
}


def _decode_wifi(wifi: vehicle_pb2.NetworkState.Wifi) -> dict[str, Any]:
    """Decode NetworkState.wifi."""
    result: dict[str, Any] = {}
    if (v := _present(wifi, "wpa_status")) is not None:
        result["wifiWpaStatus"] = _enum(_WPA_STATUS_MAP, v, what="wifi WPA status")
    if (v := _present(wifi, "ssid")) is not None:
        result["wifiSsid"] = v
    if (v := _present(wifi, "antenna_bars")) is not None:
        result["wifiAntennaBars"] = _enum(
            _CONNECTIVITY_LEVEL_MAP, v, what="wifi antenna bars"
        )
    if (v := _present(wifi, "signal")) is not None:
        result["wifiSignal"] = v
    if (v := _present(wifi, "link_speed")) is not None:
        result["wifiLinkSpeed"] = v
    if (v := _present(wifi, "freq")) is not None:
        result["wifiFreq"] = v
    if (v := _present(wifi, "secure_status")) is not None:
        result["wifiSecureStatus"] = _enum(_WIFI_SECURITY_MAP, v, what="wifi security")
    return result


def _decode_cellular(cellular: vehicle_pb2.NetworkState.Cellular) -> dict[str, Any]:
    """Decode NetworkState.cellular."""
    result: dict[str, Any] = {}
    if (v := _present(cellular, "carrier")) is not None:
        result["cellularCarrier"] = v
    if (v := _present(cellular, "mode")) is not None:
        result["cellularMode"] = v
    if (v := _present(cellular, "antenna_bars")) is not None:
        result["cellularAntennaBars"] = _enum(
            _CONNECTIVITY_LEVEL_MAP, v, what="cellular antenna bars"
        )
    if (v := _present(cellular, "signal_strength")) is not None:
        result["cellularSignalStrength"] = v
    return result


@RVMDecoder.register("vehicle.network.state", vehicle_pb2.NetworkState)
def decode_network_state(m: vehicle_pb2.NetworkState) -> dict[str, Any]:
    """vehicle.network.state — wifi and cellular status.

    Fields:
        wifiWpaStatus, wifiSsid, wifiAntennaBars, wifiSecureStatus: str
        wifiSignal: int (dBm; -255 = no reading)
        wifiLinkSpeed: int (Mbps)
        wifiFreq: int (MHz)
        cellularCarrier, cellularMode, cellularAntennaBars: str
        cellularSignalStrength: int (dBm; -255 = no reading)
    """
    result: dict[str, Any] = {}
    if m.HasField("wifi"):
        result.update(_decode_wifi(m.wifi))
    if m.HasField("cellular"):
        result.update(_decode_cellular(m.cellular))
    return result


@RVMDecoder.register("vehicle.setting.network", vehicle_pb2.NetworkState)
def decode_network_setting(m: vehicle_pb2.NetworkState) -> dict[str, Any]:
    """vehicle.setting.network — a stale network snapshot.

    Fields:
        wifiBssid: str — the access point's MAC address
        wifiMacAddress: str — the vehicle's MAC address
        wifiIpAddresses: list[str]

    Only fields vehicle.network.state lacks, so stale values can't
    overwrite live ones.
    """
    if not m.HasField("wifi"):
        return {}
    wifi = m.wifi
    result: dict[str, Any] = {}
    if (v := _present(wifi, "bssid")) is not None:
        result["wifiBssid"] = v
    if (v := _present(wifi, "mac_address")) is not None:
        result["wifiMacAddress"] = v
    if addresses := [
        address
        for entry in wifi.ip_addresses
        for address in (entry.ipv4, entry.ipv6)
        if address
    ]:
        result["wifiIpAddresses"] = addresses
    return result
