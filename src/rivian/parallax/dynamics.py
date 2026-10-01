"""Decoders for `dynamics.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from ..utils import from_epoch
from .core import _LOGGER, RVMDecoder, _enum, _present
from .proto import dynamics_pb2

_DRIVE_MODE_MAP: Final[dict[int, str]] = {
    1: "init_mode",
    2: "everyday",
    3: "off_road_snow_ice",
    4: "off_road_sport_auto",
    5: "off_road_sport_drift",
    6: "sport_launch",
    7: "fault",
    8: "sport",
    9: "distance",
    10: "towing",
    11: "off_road_auto",
    12: "off_road_sand",
    13: "off_road_rocks",
    14: "off_road_mud",
    15: "winter",
}

_GEAR_MAP: Final[dict[int, str]] = {
    0: "not_defined",
    1: "park",
    2: "reverse",
    3: "neutral",
    4: "drive",
}

_KNOWN_LOCATION_MAP: Final[dict[int, str]] = {
    1: "unknown",
    2: "home",
    3: "work",
}

_RANGE_THRESHOLD_MAP: Final[dict[int, str]] = {
    1: "normal",
    2: "low",
    3: "red",
    4: "critically_low",
}

_TEMPERATURE_IMPACT_MAP: Final[dict[int, str]] = {
    1: "normal_range",
    2: "cold_may_impact",
    3: "cold_impact",
}

_TIRE_POSITION_MAP: Final[dict[int, str]] = {
    1: "FrontLeft",
    2: "FrontRight",
    3: "RearLeft",
    4: "RearRight",
}


@RVMDecoder.register("dynamics.vehicle.drive_mode", dynamics_pb2.DriveMode)
def decode_drive_mode(m: dynamics_pb2.DriveMode) -> dict[str, Any]:
    """dynamics.vehicle.drive_mode — active drive mode and cold-weather limits.

    Fields:
        driveMode: str
        limitedAccelCold, limitedRegenCold: int — raw flags
    """
    return {
        "driveMode": _enum(_DRIVE_MODE_MAP, _present(m, "mode"), what="drive mode"),
        "limitedAccelCold": _present(m, "limited_accel_cold"),
        "limitedRegenCold": _present(m, "limited_regen_cold"),
    }


@RVMDecoder.register("dynamics.vehicle.gear", dynamics_pb2.Gear)
def decode_gear(m: dynamics_pb2.Gear) -> dict[str, Any]:
    """dynamics.vehicle.gear — current gear.

    Fields:
        gearStatus: str
    """
    return {"gearStatus": _enum(_GEAR_MAP, _present(m, "gear"), what="gear")}


@RVMDecoder.register("dynamics.vehicle.gnss", dynamics_pb2.Gnss)
def decode_gnss(m: dynamics_pb2.Gnss) -> dict[str, Any]:
    """dynamics.vehicle.gnss — GPS position, altitude and bearing.

    Fields:
        gnssTimeStamp: datetime — time of the fix
        gnssLocation: {"latitude": float, "longitude": float, "timeStamp": datetime}
            (the gateway's VehicleLocation shape)
        gnssAltitude: float (meters)
        gnssBearing: float (degrees)
    """
    lat = _present(m, "latitude")
    lon = _present(m, "longitude")
    alt = _present(m, "altitude")
    bearing = _present(m, "bearing")
    epoch = _present(m, "time")
    fix_time = from_epoch(epoch) if epoch is not None else None

    result: dict[str, Any] = {}
    if fix_time is not None:
        result["gnssTimeStamp"] = fix_time
    if lat is not None and lon is not None:
        location: dict[str, Any] = {
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
        }
        if fix_time is not None:
            location["timeStamp"] = fix_time
        result["gnssLocation"] = location
    if alt is not None:
        result["gnssAltitude"] = round(alt, 1)
    if bearing is not None:
        result["gnssBearing"] = round(bearing, 1)
    return result


@RVMDecoder.register("dynamics.vehicle.location", dynamics_pb2.KnownLocation)
def decode_known_location(m: dynamics_pb2.KnownLocation) -> dict[str, Any]:
    """dynamics.vehicle.location — whether the vehicle is at a known place.

    Fields:
        knownLocation: str ("unknown" | "home" | "work")
    """
    return {
        "knownLocation": _enum(
            _KNOWN_LOCATION_MAP, _present(m, "location"), what="known location"
        )
    }


@RVMDecoder.register("dynamics.vehicle.odometer", dynamics_pb2.Odometer)
def decode_odometer(m: dynamics_pb2.Odometer) -> dict[str, Any]:
    """dynamics.vehicle.odometer — total distance traveled.

    Fields:
        vehicleMileage: float (meters)
    """
    if (v := _present(m, "distance")) is None:
        return {}
    return {"vehicleMileage": v * 1000}  # km -> meters


@RVMDecoder.register("dynamics.vehicle.range", dynamics_pb2.Range)
def decode_range(m: dynamics_pb2.Range) -> dict[str, Any]:
    """dynamics.vehicle.range — remaining range and cold-weather impact.

    Fields:
        distanceToEmpty: int (km)
        rangeThreshold: str
        coldRangeNotification: str
    """
    return {
        "distanceToEmpty": _present(m, "distance_to_empty"),
        "rangeThreshold": _enum(
            _RANGE_THRESHOLD_MAP, _present(m, "threshold"), what="range threshold"
        ),
        "coldRangeNotification": _enum(
            _TEMPERATURE_IMPACT_MAP,
            _present(m, "temperature_impact"),
            what="range temperature impact",
        ),
    }


@RVMDecoder.register("dynamics.tires.state", dynamics_pb2.TiresState)
def decode_tires(m: dynamics_pb2.TiresState) -> dict[str, Any]:
    """dynamics.tires.state — per-tire pressure, status and validity.

    Fields:
        tirePressureFrontLeft, tirePressureFrontRight, etc.: float (bar)
        tirePressureStatusFrontLeft, etc.: str ("OK" | "Warning")
        tirePressureStatusValidFrontLeft, etc.: str ("valid" | "invalid")
    """
    result: dict[str, Any] = {}
    for s in m.tire:
        if s.pos not in _TIRE_POSITION_MAP:
            _LOGGER.debug("Unknown tire position %s", s.pos)
            continue
        suffix = _TIRE_POSITION_MAP[s.pos]

        # Pressure and status are stale while invalid.
        valid = not s.invalid
        result[f"tirePressureStatusValid{suffix}"] = "valid" if valid else "invalid"
        if not valid:
            continue

        if (pressure := _present(s, "pressure")) is not None:
            result[f"tirePressure{suffix}"] = pressure
        if (status_val := _present(s, "status")) is not None:
            result[f"tirePressureStatus{suffix}"] = (
                "OK" if status_val == dynamics_pb2.TIRE_PRESSURE_OK else "Warning"
            )
    return result


@RVMDecoder.register("dynamics.vehicle.efficiency", dynamics_pb2.Efficiency)
def decode_efficiency(m: dynamics_pb2.Efficiency) -> dict[str, Any]:
    """dynamics.vehicle.efficiency — energy efficiency.

    Fields:
        vehicleEfficiency: int (Wh/km) — what range estimates use
        _efficiencyField2: int (Wh/km, inferred) — unknown
        _efficiencyHistory: list[int] (Wh/km, inferred) — ten values,
            possibly recent trips
    """
    result: dict[str, Any] = {}
    if (v := _present(m, "efficiency")) is not None:
        result["vehicleEfficiency"] = v
    if (v := _present(m, "field_2")) is not None:
        result["_efficiencyField2"] = v
    if history := sorted(m.history, key=lambda entry: entry.index):
        result["_efficiencyHistory"] = [entry.value for entry in history]
    return result


@RVMDecoder.register("dynamics.vehicle.mass_estimate", dynamics_pb2.MassEstimate)
def decode_mass_estimate(m: dynamics_pb2.MassEstimate) -> dict[str, Any]:
    """dynamics.vehicle.mass_estimate — the vehicle's estimated mass.

    Fields:
        vehicleMassEstimate: int (kg)
    """
    if (v := _present(m, "mass")) is None:
        return {}
    return {"vehicleMassEstimate": v}


@RVMDecoder.register("dynamics.brakes.fluid_level", dynamics_pb2.BrakeFluidLevel)
def decode_brake_fluid_level(m: dynamics_pb2.BrakeFluidLevel) -> dict[str, Any]:
    """dynamics.brakes.fluid_level — brake fluid level.

    Fields:
        _brakeFluidLevel: int — raw (1 so far, presumably normal)
    """
    if (v := _present(m, "field_1")) is None:
        return {}
    return {"_brakeFluidLevel": v}
