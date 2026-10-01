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
        vehicle.PowerState(state=state),  # type: ignore[arg-type]
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
        "wifiSignal": -55,
        "cellularCarrier": "Carrier",
        "cellularMode": "LTE",
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
