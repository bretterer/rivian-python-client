"""Tests for the `dynamics.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import dynamics_pb2 as dynamics

from .helpers import decode, epoch


def test_gnss() -> None:
    """The fix time applies to the whole message and is repeated on the location."""
    ms = 1790553428211
    result = decode(
        "dynamics.vehicle.gnss",
        dynamics.Gnss(
            latitude=33.0834,
            longitude=-80.1465,
            altitude=1630.12,
            bearing=254.1,
            time=ms,
        ),
    )
    assert result == {
        "gnssTimeStamp": epoch(ms),
        "gnssLocation": {
            "latitude": 33.0834,
            "longitude": -80.1465,
            "timeStamp": epoch(ms),
        },
        "gnssAltitude": 1630.1,
        "gnssBearing": 254.1,
    }


def test_gnss_empty() -> None:
    """An empty payload has no fix, so nothing is reported."""
    assert decode("dynamics.vehicle.gnss") == {}


def test_drive_mode_and_gear() -> None:
    """Drive mode and gear map to their enum strings."""
    mode = decode(
        "dynamics.vehicle.drive_mode",
        dynamics.DriveMode(mode=dynamics.DRIVE_MODE_DISTANCE),
    )
    assert mode["driveMode"] == "distance"
    gear = decode("dynamics.vehicle.gear", dynamics.Gear(gear=dynamics.GEAR_PARK))
    assert gear == {"gearStatus": "park"}


def test_odometer() -> None:
    """Odometer km is reported in meters."""
    result = decode("dynamics.vehicle.odometer", dynamics.Odometer(distance=17114))
    assert result == {"vehicleMileage": 17114000}


def test_range() -> None:
    """Distance to empty and its threshold/temperature flags."""
    result = decode(
        "dynamics.vehicle.range",
        dynamics.Range(
            distance_to_empty=344,
            threshold=dynamics.RANGE_NORMAL,
            temperature_impact=dynamics.TEMPERATURE_COLD_IMPACT,
        ),
    )
    assert result == {
        "distanceToEmpty": 344,
        "rangeThreshold": "normal",
        "coldRangeNotification": "cold_impact",
    }


def test_tires() -> None:
    """Valid tires report pressure and status; invalid ones report only validity."""
    tire = dynamics.TiresState.Tire
    result = decode(
        "dynamics.tires.state",
        dynamics.TiresState(
            tire=[
                tire(
                    pos=dynamics.TIRE_FRONT_LEFT,
                    status=dynamics.TIRE_PRESSURE_OK,
                    pressure=3.48,
                ),
                tire(
                    pos=dynamics.TIRE_FRONT_RIGHT,
                    status=dynamics.TIRE_PRESSURE_WARNING,
                    pressure=2.1,
                    invalid=True,
                ),
            ]
        ),
    )
    assert result == {
        "tirePressureStatusValidFrontLeft": "valid",
        "tirePressureFrontLeft": 3.48,
        "tirePressureStatusFrontLeft": "OK",
        "tirePressureStatusValidFrontRight": "invalid",
    }


def test_efficiency() -> None:
    """Efficiency (Wh/km) plus the history in index order."""
    entry = dynamics.Efficiency.History
    result = decode(
        "dynamics.vehicle.efficiency",
        dynamics.Efficiency(
            efficiency=252,
            field_2=293,
            history=[entry(index=2, value=491), entry(index=1, value=446)],
        ),
    )
    assert result == {
        "vehicleEfficiency": 252,
        "_efficiencyField2": 293,
        "_efficiencyHistory": [446, 491],
    }


def test_mass_estimate() -> None:
    """Estimated mass in kg."""
    result = decode("dynamics.vehicle.mass_estimate", dynamics.MassEstimate(mass=3250))
    assert result == {"vehicleMassEstimate": 3250}


def test_brake_fluid_level() -> None:
    """The raw brake fluid value."""
    result = decode("dynamics.brakes.fluid_level", dynamics.BrakeFluidLevel(field_1=1))
    assert result == {"_brakeFluidLevel": 1}
