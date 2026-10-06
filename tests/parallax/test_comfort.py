"""Tests for the `comfort.*` decoders."""

from __future__ import annotations

import pytest

from rivian.parallax.proto import comfort_pb2 as comfort

from .helpers import decode


def test_cabin_temperatures() -> None:
    """Interior temperature and the driver-zone set point."""
    result = decode(
        "comfort.cabin.cabin_temperatures",
        comfort.CabinTemperatures(interior_temperature=31.0, driver_set_point=21.5),
    )
    assert result == {
        "cabinClimateInteriorTemperature": 31.0,
        "cabinClimateDriverTemperature": 21.5,
    }


def test_cabin_temperatures_without_set_point() -> None:
    """A vehicle that doesn't send the set point reports None, not 0 °C."""
    result = decode(
        "comfort.cabin.cabin_temperatures",
        comfort.CabinTemperatures(interior_temperature=32.4),
    )
    assert result == {
        "cabinClimateInteriorTemperature": 32.4,
        "cabinClimateDriverTemperature": None,
    }


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (comfort.PRECONDITIONING_INITIATE, "initiate"),
        (comfort.PRECONDITIONING_ACTIVE, "active"),
        (comfort.PRECONDITIONING_COMPLETE_MAINTAIN, "complete_maintain"),
        (comfort.PRECONDITIONING_UNAVAILABLE, "unavailable"),
        (comfort.PRECONDITIONING_STATUS_UNSPECIFIED, "undefined"),
    ],
)
def test_preconditioning(status: int, expected: str) -> None:
    """Statuses use the GraphQL values; the type is None when unset."""
    result = decode(
        "comfort.cabin.cabin_preconditioning_status",
        comfort.CabinPreconditioningStatus(status=status),  # type: ignore[arg-type]
    )
    assert result == {
        "cabinPreconditioningStatus": expected,
        "cabinPreconditioningType": None,
    }


def test_preconditioning_type() -> None:
    """The preconditioning type maps to its GraphQL value."""
    result = decode(
        "comfort.cabin.cabin_preconditioning_status",
        comfort.CabinPreconditioningStatus(
            status=comfort.PRECONDITIONING_ACTIVE,
            type=comfort.PRECONDITIONING_TYPE_USER_SELECTED,
        ),
    )
    assert result["cabinPreconditioningType"] == "user_selected"


def test_defrost() -> None:
    """Defrost and Off by value; an empty payload is unknown."""
    rvm = "comfort.cabin.defrost_defog_status"
    active = comfort.DefrostDefogStatus(status=comfort.DEFROST_ACTIVE)
    off = comfort.DefrostDefogStatus(status=comfort.DEFROST_OFF)
    assert decode(rvm, active) == {"defrostDefogStatus": "Defrost"}
    assert decode(rvm, off) == {"defrostDefogStatus": "Off"}
    assert decode(rvm) == {"defrostDefogStatus": None}


def test_climate_hold_status() -> None:
    """The end time is read from its {seconds} wrapper."""
    status = comfort.ClimateHoldStatus
    result = decode(
        "comfort.cabin.climate_hold_status",
        status(
            status=comfort.CLIMATE_HOLD_STATUS_ON,
            availability=comfort.CLIMATE_HOLD_AVAILABLE,
            end_time=status.EndTime(seconds=1790000000),
        ),
    )
    assert result == {
        "climateHoldStatus": "on",
        "climateHoldAvailability": "available",
        "climateHoldUnavailabilityReason": None,
        "climateHoldEndTime": 1790000000,
    }


def test_pet_mode_status_defaults() -> None:
    """An empty payload reads as the proto3 zero values, not unknown."""
    assert decode("comfort.cabin.pet_mode_status") == {
        "petModeStatus": "off",
        "petModeTemperatureStatus": "default",
        "petModeCabinClimate": "comfortable",
    }


def test_seat_conditioning() -> None:
    """Heat/vent levels combine surface and type; no state means off."""
    surface = comfort.SeatConditioningStatus.Surface
    heat = comfort.CONDITIONING_HEAT
    result = decode(
        "comfort.cabin.seat_conditioning_status",
        comfort.SeatConditioningStatus(
            surface=[
                surface(
                    id=comfort.SEAT_ROW_1_LEFT,
                    type=heat,
                    state=comfort.CONDITIONING_LEVEL_2,
                ),
                surface(
                    id=comfort.STEERING_WHEEL,
                    type=heat,
                    state=comfort.CONDITIONING_LEVEL_1,
                ),
                surface(
                    id=comfort.SEAT_ROW_3_RIGHT,
                    type=heat,
                    state=comfort.CONDITIONING_LEVEL_3,
                ),
                surface(id=comfort.SEAT_ROW_2_LEFT, type=heat),
            ]
        ),
    )
    assert result == {
        "seatFrontLeftHeat": "Level_2",
        "steeringWheelHeat": "Level_1",
        "seatThirdRowRightHeat": "Level_3",
        "seatRearLeftHeat": "Off",
    }


def test_user_modes_car_wash() -> None:
    """Car wash mode is on when set and off when left out."""
    rvm = "comfort.user_modes.state"
    on = decode(rvm, comfort.UserModesState(car_wash_mode=True, camp_mode=2))
    assert on["carWashMode"] == "on"
    assert on["serviceMode"] == "off"
    assert on["_campMode"] == 2
    assert decode(rvm)["carWashMode"] == "off"
