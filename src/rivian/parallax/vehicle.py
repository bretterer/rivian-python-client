"""Decoders for `vehicle.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import vehicle_pb2

_POWER_STATE_MAP: Final[dict[int, str]] = {
    vehicle_pb2.POWER_SLEEP: "sleep",
    vehicle_pb2.POWER_STANDBY: "standby",
    vehicle_pb2.POWER_READY: "ready",
    vehicle_pb2.POWER_GO: "go",
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


@RVMDecoder.register("vehicle.power.state", vehicle_pb2.VehiclePowerState)
def decode_power_state(m: vehicle_pb2.VehiclePowerState) -> dict[str, Any]:
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
            savedTireOdometerDelta, odometerAtLastRotation,
            savedOdometerAtLastRotationDelta, rotationReminderInterval,
            isInstalled, tires, currentOdometer (distances in meters; the
            saved deltas are only set on an uninstalled wheel set)
        wheelsInstalled: int — how many are installed
    """
    wheels = [
        {
            "wheelPackage": w.wheel_package,
            "tireOdometer": w.tire_odometer,
            "savedTireOdometerDelta": w.saved_tire_odometer_delta,
            "odometerAtLastRotation": w.odometer_at_last_rotation,
            "savedOdometerAtLastRotationDelta": (
                w.saved_odometer_at_last_rotation_delta
            ),
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
    vehicle_pb2.CONNECTIVITY_LEVEL_0: "level_0",
    vehicle_pb2.CONNECTIVITY_LEVEL_1: "level_1",
    vehicle_pb2.CONNECTIVITY_LEVEL_2: "level_2",
    vehicle_pb2.CONNECTIVITY_LEVEL_3: "level_3",
    vehicle_pb2.CONNECTIVITY_LEVEL_4: "level_4",
}

_ACTIVE_INTERFACE_MAP: Final[dict[int, str]] = {
    vehicle_pb2.ACTIVE_INTERFACE_WIFI: "wifi",
    vehicle_pb2.ACTIVE_INTERFACE_CELLULAR: "cellular",
}

_WIFI_SECURITY_MAP: Final[dict[int, str]] = {
    vehicle_pb2.WIFI_OPEN: "open",
    vehicle_pb2.WIFI_WPA_PERSONAL: "wpa_personal",
    vehicle_pb2.WIFI_WPA_ENTERPRISE: "wpa_enterprise",
    vehicle_pb2.WIFI_WPA2_PERSONAL: "wpa2_personal",
    vehicle_pb2.WIFI_WPA2_ENTERPRISE: "wpa2_enterprise",
}

_WPA_STATUS_MAP: Final[dict[int, str]] = {
    vehicle_pb2.WPA_NOT_CONNECTED: "not_connected",
    vehicle_pb2.WPA_CONNECTED: "connected",
    vehicle_pb2.WPA_SCANNING: "scanning",
    vehicle_pb2.WPA_CONNECTING: "connecting",
    vehicle_pb2.WPA_DISCONNECTING: "disconnecting",
}


def _decode_wifi(wifi: vehicle_pb2.NetworkState.Wifi) -> dict[str, Any]:
    """Decode NetworkState.wifi; unset enums and strings are None."""
    return {
        "wifiWpaStatus": _enum(
            _WPA_STATUS_MAP, wifi.wpa_status or None, what="wifi WPA status"
        ),
        "wifiSsid": wifi.ssid or None,
        "wifiAntennaBars": _enum(
            _CONNECTIVITY_LEVEL_MAP, wifi.antenna_bars or None, what="wifi antenna bars"
        ),
        "wifiSignal": wifi.signal,
        "wifiLinkSpeed": wifi.link_speed,
        "wifiFreq": wifi.freq,
        "wifiSecureStatus": _enum(
            _WIFI_SECURITY_MAP, wifi.secure_status or None, what="wifi security"
        ),
    }


def _decode_cellular(cellular: vehicle_pb2.NetworkState.Cellular) -> dict[str, Any]:
    """Decode NetworkState.cellular; unset enums and strings are None."""
    return {
        "cellularCarrier": cellular.carrier or None,
        "cellularMode": cellular.mode or None,
        "cellularAntennaBars": _enum(
            _CONNECTIVITY_LEVEL_MAP,
            cellular.antenna_bars or None,
            what="cellular antenna bars",
        ),
        "cellularSignalStrength": cellular.signal_strength,
    }


@RVMDecoder.register("vehicle.network.state", vehicle_pb2.NetworkState)
def decode_network_state(m: vehicle_pb2.NetworkState) -> dict[str, Any]:
    """vehicle.network.state — wifi and cellular status.

    Fields:
        networkActiveInterface: str | None ("wifi" | "cellular"); inferred
        networkAntennaBars: str | None — the active connection's level;
            inferred
        wifiWpaStatus, wifiSsid, wifiAntennaBars, wifiSecureStatus: str
        wifiSignal: int (dBm; -255 = no reading)
        wifiLinkSpeed: int (Mbps)
        wifiFreq: int (MHz)
        cellularCarrier, cellularMode, cellularAntennaBars: str
        cellularSignalStrength: int (dBm; -255 = no reading)
    """
    result: dict[str, Any] = {
        "networkActiveInterface": _enum(
            _ACTIVE_INTERFACE_MAP,
            m.active_interface or None,
            what="active network interface",
        ),
        "networkAntennaBars": _enum(
            _CONNECTIVITY_LEVEL_MAP,
            m.connectivity_level or None,
            what="network antenna bars",
        ),
    }
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
