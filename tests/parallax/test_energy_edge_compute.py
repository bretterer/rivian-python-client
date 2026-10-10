"""Tests for the `energy_edge_compute.*` decoders."""

from __future__ import annotations

from typing import Any

import pytest

from rivian.parallax.proto import (
    charging_pb2 as charging,
    energy_edge_compute_pb2 as eec,
)

from .helpers import decode, epoch


def test_cold_weather_soc() -> None:
    """The graph's green and blue values plus the cold range impact."""
    result = decode(
        "energy_edge_compute.graphs.cold_weather_soc",
        eec.ColdWeatherSoc(soc_perc_green=70, soc_perc_blue=62, cold_range_impact=25),
    )
    assert result == {
        "coldWeatherSoc": 70,
        "coldWeatherSocBlue": 62,
        "coldRangeImpact": 25,
    }


def test_parked_energy_distributions() -> None:
    """Each window is a nested dict with its duration; unsent measures are 0."""
    window = eec.ParkedEnergyDistributions.EnergyDistribution
    result = decode(
        "energy_edge_compute.graphs.parked_energy_distributions",
        eec.ParkedEnergyDistributions(
            last_24_hours=window(total_energy=1.5, total_range=5.9524, duration=1440),
            last_park_session=window(total_energy=0.9, duration=896),
        ),
    )
    zeros = dict.fromkeys(
        (
            "totalEnergy",
            "thermalEnergy",
            "outletsEnergy",
            "systemEnergy",
            "gearGuardEnergy",
            "totalRange",
            "thermalRange",
            "outletsRange",
            "systemRange",
            "gearGuardRange",
        ),
        0.0,
    )
    assert result == {
        "parkedEnergyLast24Hours": {
            **zeros,
            "totalEnergy": 1.5,
            "totalRange": 5.9524,
            "duration": 1440,
        },
        "parkedEnergyLastParkSession": {**zeros, "totalEnergy": 0.9, "duration": 896},
    }


def test_charge_session_breakdown() -> None:
    """Live stats use the vehicle's own range figures."""
    result = decode(
        "energy_edge_compute.graphs.charge_session_breakdown",
        eec.ChargeSessionBreakdown(
            total_energy=6.3,
            pack_energy=6.2,
            system_energy=0.1,
            active_charging_time=36,
            time_remaining=12,
            range_added=38,
            power=11.1,
            range_rate=41,
            is_free_session=True,
            charging_state=3,  # type: ignore[arg-type]
        ),
    )
    assert result == {
        "totalChargedEnergy": pytest.approx(6.3),
        "chargeSessionPower": pytest.approx(11.1),
        "rangeAddedThisSession": 38.0,
        "kilometersChargedPerHour": 41.0,
        "chargeSessionTimeToEndOfCharge": 12,
        "activeChargingTime": 36,
        "packEnergy": pytest.approx(6.2),
        "thermalEnergy": 0.0,
        "outletsEnergy": 0.0,
        "systemEnergy": pytest.approx(0.1),
        "isFreeSession": True,
        "chargeSessionChargerState": "charging_active",
    }


def test_charge_session_breakdown_cost() -> None:
    """A reported session cost becomes a decimal price and currency."""
    breakdown = eec.ChargeSessionBreakdown
    result = decode(
        "energy_edge_compute.graphs.charge_session_breakdown",
        breakdown(
            session_cost=breakdown.Money(
                currency_code="USD", units=4, nanos=250_000_000
            )
        ),
    )
    assert result["currentPrice"] == pytest.approx(4.25)
    assert result["currentCurrency"] == "USD"
    assert result["isFreeSession"] is False


def test_charge_session_breakdown_fresh_session() -> None:
    """Absent fields are zeros, and a stale rate is zeroed while power is 0."""
    result = decode(
        "energy_edge_compute.graphs.charge_session_breakdown",
        eec.ChargeSessionBreakdown(range_rate=8, is_free_session=True),
    )
    assert result == {
        "totalChargedEnergy": 0.0,
        "chargeSessionPower": 0.0,
        "rangeAddedThisSession": 0.0,
        "kilometersChargedPerHour": 0.0,
        "chargeSessionTimeToEndOfCharge": 0,
        "activeChargingTime": 0,
        "packEnergy": 0.0,
        "thermalEnergy": 0.0,
        "outletsEnergy": 0.0,
        "systemEnergy": 0.0,
        "isFreeSession": True,
    }


_T0 = 1785695977217


def _segment(
    start_ms: int, end_ms: int, state: int, power: float = 0.0
) -> eec.ChargingGraphGlobal.Segment:
    return eec.ChargingGraphGlobal.Segment(
        soc=72,
        power=power,
        start_time=start_ms,
        end_time=end_ms,
        state=state,  # type: ignore[arg-type]
    )


def _graph(*segments: eec.ChargingGraphGlobal.Segment) -> dict[str, Any]:
    return decode(
        "energy_edge_compute.graphs.charging_graph_global",
        eec.ChargingGraphGlobal(segment=segments),
    )


def test_charging_graph_global_active() -> None:
    """The latest segment's power is reported, with active time summed."""
    result = _graph(_segment(_T0, _T0 + 60_000, charging.CHARGING_ACTIVE, 5.8))
    assert result["startTime"] == epoch(_T0)
    assert result["timeElapsed"] == 60
    assert result["chargingGraphPower"] == pytest.approx(5.8)


def test_charging_graph_global_stopped_and_resumed() -> None:
    """Only active segments count toward elapsed time; a stopped tail reads 0 kW."""
    charged = _segment(_T0, _T0 + 60_000, charging.CHARGING_ACTIVE, 5.8)
    stopped = _segment(_T0 + 60_000, _T0 + 660_000, charging.CHARGING_USER_STOPPED)
    resumed = _segment(_T0 + 660_000, _T0 + 780_000, charging.CHARGING_ACTIVE, 5.8)

    result = _graph(charged, stopped)
    assert result["timeElapsed"] == 60
    assert result["chargingGraphPower"] == 0.0
    assert result["chargingGraphKilometersChargedPerHour"] == 0.0

    result = _graph(charged, stopped, resumed)
    assert result["timeElapsed"] == 180
    assert result["chargingGraphPower"] == pytest.approx(5.8)


def test_charging_graph_global_empty() -> None:
    """A new session's empty graph yields nothing."""
    assert _graph() == {}
