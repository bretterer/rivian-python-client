"""Tests for the `vehicle.*` decoders."""

from __future__ import annotations

import pytest

from rivian.parallax.proto import vehicle_pb2 as vehicle

from .helpers import decode


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (vehicle.POWER_GO, "go"),
        (vehicle.POWER_SLEEP, "sleep"),
        (9, "standby"),  # unmapped values fall back to standby
    ],
)
def test_power_state(state: int, expected: str) -> None:
    """Known states map; unknown values fall back to standby."""
    result = decode(
        "vehicle.power.state",
        vehicle.VehiclePowerState(state=state),  # type: ignore[arg-type]
    )
    assert result == {"powerState": expected}


def test_network_state() -> None:
    """Strings decode as text and signed dBm values come back negative."""
    state = vehicle.NetworkState
    result = decode(
        "vehicle.network.state",
        state(
            wifi=state.Wifi(wpa_status=vehicle.WPA_CONNECTED, ssid="Home", signal=-55),
            cellular=state.Cellular(
                carrier="Carrier", mode="LTE", signal_strength=-255
            ),
        ),
    )
    assert result == {
        "wifiWpaStatus": "connected",
        "wifiSsid": "Home",
        "wifiAntennaBars": None,
        "wifiSignal": -55,
        "wifiLinkSpeed": 0,
        "wifiFreq": 0,
        "wifiSecureStatus": None,
        "cellularCarrier": "Carrier",
        "cellularMode": "LTE",
        "cellularAntennaBars": None,
        "cellularSignalStrength": -255,
    }


def test_network_setting() -> None:
    """Only the fields the live network topic doesn't carry are surfaced."""
    state = vehicle.NetworkState
    result = decode(
        "vehicle.setting.network",
        state(
            wifi=state.Wifi(
                ssid="Home",
                signal=-60,
                bssid="00:11:22:33:44:55",
                mac_address="66:77:88:99:aa:bb",
                ip_addresses=[
                    state.IpAddress(ipv4="192.168.1.20"),
                    state.IpAddress(ipv6=""),
                ],
            )
        ),
    )
    assert result == {
        "wifiBssid": "00:11:22:33:44:55",
        "wifiMacAddress": "66:77:88:99:aa:bb",
        "wifiIpAddresses": ["192.168.1.20"],
    }


def test_wheels() -> None:
    """Each wheel set decodes, and installed ones are counted."""
    wheels = vehicle.VehicleWheels
    result = decode(
        "vehicle.wheels.vehicle_wheels",
        wheels(
            wheel=[
                wheels.Wheel(wheel_package=1, is_installed=True, tire_odometer=5000),
                wheels.Wheel(
                    wheel_package=2,
                    saved_tire_odometer_delta=1200,
                    saved_odometer_at_last_rotation_delta=300,
                ),
            ]
        ),
    )
    assert result["wheelsInstalled"] == 1
    assert result["wheels"][0]["tireOdometer"] == 5000
    assert result["wheels"][1]["savedTireOdometerDelta"] == 1200
    assert result["wheels"][1]["savedOdometerAtLastRotationDelta"] == 300
