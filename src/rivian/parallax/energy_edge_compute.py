"""Decoders for `energy_edge_compute.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from ..utils import from_epoch
from .charging import _CHARGING_STATE_MAP
from .core import RVMDecoder, _enum
from .proto import charging_pb2, energy_edge_compute_pb2


@RVMDecoder.register(
    "energy_edge_compute.graphs.cold_weather_soc",
    energy_edge_compute_pb2.ColdWeatherSoc,
)
def decode_cold_weather_soc(
    m: energy_edge_compute_pb2.ColdWeatherSoc,
) -> dict[str, Any]:
    """energy_edge_compute.graphs.cold_weather_soc — the app's cold-weather graph.

    Fields:
        coldWeatherSoc: int (percent; the graph's green value)
        coldWeatherSocBlue: int (percent; the graph's blue value)
        coldRangeImpact: int (km)
    """
    return {
        "coldWeatherSoc": m.soc_perc_green,
        "coldWeatherSocBlue": m.soc_perc_blue,
        "coldRangeImpact": m.cold_range_impact,
    }


# EnergyDistribution field -> result key.
_ENERGY_DISTRIBUTION_MAP: Final[dict[str, str]] = {
    "total_energy": "totalEnergy",
    "thermal_energy": "thermalEnergy",
    "outlets_energy": "outletsEnergy",
    "system_energy": "systemEnergy",
    "gear_guard_energy": "gearGuardEnergy",
    "total_range": "totalRange",
    "thermal_range": "thermalRange",
    "outlets_range": "outletsRange",
    "system_range": "systemRange",
    "gear_guard_range": "gearGuardRange",
}


# ParkedEnergyDistributions field -> result key.
_PARKED_ENERGY_WINDOWS: Final[dict[str, str]] = {
    "last_24_hours": "parkedEnergyLast24Hours",
    "last_8_hours": "parkedEnergyLast8Hours",
    "last_park_session": "parkedEnergyLastParkSession",
}


@RVMDecoder.register(
    "energy_edge_compute.graphs.parked_energy_distributions",
    energy_edge_compute_pb2.ParkedEnergyDistributions,
)
def decode_parked_energy_distributions(
    m: energy_edge_compute_pb2.ParkedEnergyDistributions,
) -> dict[str, Any]:
    """energy_edge_compute.graphs.parked_energy_distributions — parked energy use.

    Fields:
        parkedEnergyLast24Hours, parkedEnergyLast8Hours,
        parkedEnergyLastParkSession: dict[str, float] — kWh and range (km)
            per consumer, plus `duration` (minutes; counts up for the park
            session)
    """
    result: dict[str, Any] = {}
    for field, key in _PARKED_ENERGY_WINDOWS.items():
        if not m.HasField(field):
            continue
        distribution = getattr(m, field)
        window: dict[str, float] = {
            measure_key: round(getattr(distribution, measure), 4)
            for measure, measure_key in _ENERGY_DISTRIBUTION_MAP.items()
        }
        window["duration"] = distribution.duration
        result[key] = window
    return result


# The charging graph has no range figures; ~3.5 km/kWh is a typical average.
_FALLBACK_KM_PER_KWH: Final = 3.5


@RVMDecoder.register(
    "energy_edge_compute.graphs.charge_session_breakdown",
    energy_edge_compute_pb2.ChargeSessionBreakdown,
)
def decode_charge_session_breakdown(
    m: energy_edge_compute_pb2.ChargeSessionBreakdown,
) -> dict[str, Any]:
    """energy_edge_compute.graphs.charge_session_breakdown — live charge session stats.

    Fields:
        totalChargedEnergy: float (kWh)
        power: float (kW)
        rangeAddedThisSession: float (km)
        kilometersChargedPerHour: float (km of range per hour; 0 while
            power is 0, since it can be stale)
        timeToEndOfCharge: int (minutes)
        activeChargingTime: int (minutes; pauses while stopped/scheduled)
        packEnergy, thermalEnergy, outletsEnergy, systemEnergy: float (kWh)
        isFreeSession: bool
        currentPrice: float, currentCurrency: str — only when there's a cost
        chargerState: str — as in charging.session.status

    A session's totals survive stops and holds, and persist after plug-in
    until the next session starts. The last message before charging
    stops keeps its power and rate, so gate on charging.session.status.
    """
    power = round(m.power, 2)
    result: dict[str, Any] = {
        "totalChargedEnergy": round(m.total_energy, 4),
        "power": power,
        "rangeAddedThisSession": float(m.range_added),
        "kilometersChargedPerHour": float(m.range_rate) if power > 0 else 0.0,
        "timeToEndOfCharge": m.time_remaining,
        "activeChargingTime": m.active_charging_time,
        "packEnergy": round(m.pack_energy, 4),
        "thermalEnergy": round(m.thermal_energy, 4),
        "outletsEnergy": round(m.outlets_energy, 4),
        "systemEnergy": round(m.system_energy, 4),
        "isFreeSession": m.is_free_session,
    }
    # Empty on free sessions.
    if (cost := m.session_cost).ListFields():
        result["currentPrice"] = cost.units + cost.nanos / 1e9
        result["currentCurrency"] = cost.currency_code
    if m.HasField("charging_state"):
        result["chargerState"] = _enum(
            _CHARGING_STATE_MAP, m.charging_state, what="charging state"
        )
    return result


@RVMDecoder.register(
    "energy_edge_compute.graphs.charging_graph_global",
    energy_edge_compute_pb2.ChargingGraphGlobal,
)
def decode_charging_graph_global(
    m: energy_edge_compute_pb2.ChargingGraphGlobal,
) -> dict[str, Any]:
    """energy_edge_compute.graphs.charging_graph_global — session timeline.

    Fields:
        startTime: datetime (session start)
        timeElapsed: int (seconds spent charging)
        power: float (kW, latest segment)
        kilometersChargedPerHour: float (estimated from power)

    Power updates about once a minute; prefer charge_session_breakdown
    for live power and rate.
    """
    segments = m.segment
    if not segments:
        return {}

    active_segments = [
        s
        for s in segments
        if round(s.power, 2) > 0 or s.state == charging_pb2.CHARGING_ACTIVE
    ]
    first_seg = active_segments[0] if active_segments else segments[0]
    result: dict[str, Any] = {}

    if first_seg.start_time:
        result["startTime"] = from_epoch(first_seg.start_time)

    result["timeElapsed"] = sum(
        max(0, int((s.end_time - s.start_time) / 1000))
        for s in active_segments
        if s.end_time and s.start_time
    )

    latest_power = round(segments[-1].power, 2)
    if latest_power > 0 and segments[-1].state != charging_pb2.CHARGING_USER_STOPPED:
        result["power"] = latest_power
        result["kilometersChargedPerHour"] = round(
            latest_power * _FALLBACK_KM_PER_KWH, 1
        )
    else:
        result["power"] = 0.0
        result["kilometersChargedPerHour"] = 0.0

    return result
