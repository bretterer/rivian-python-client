"""Wire fixtures derived independently from Android 3.17.0 field definitions."""

import pytest

from rivian.const import VehicleCommand as C
from rivian.parallax.controls import encode_control_command


@pytest.mark.parametrize(
    "command,params,rvm,wire",
    [
        (
            C.VEHICLE_CABIN_PRECONDITION_ENABLE,
            None,
            "comfort.cabin.enable_preconditioning",
            "",
        ),
        (
            C.VEHICLE_CABIN_PRECONDITION_DISABLE,
            None,
            "comfort.cabin.disable_preconditioning",
            "",
        ),
        (C.START_CHARGING, None, "charging.energy.start_charging", ""),
        (C.STOP_CHARGING, None, "charging.energy.stop_charging", ""),
        (
            C.CABIN_PRECONDITIONING_SET_TEMP,
            {"HVAC_set_temp": 21},
            "comfort.cabin.set_preconditioning_temperature",
            "0d0000a841",
        ),
        (
            C.CABIN_PRECONDITIONING_SET_TEMP,
            {"HVAC_set_temp": 0},
            "comfort.cabin.set_preconditioning_temperature",
            "",
        ),
        (
            C.CABIN_PRECONDITIONING_SET_TEMP,
            {"HVAC_set_temp": 63.5},
            "comfort.cabin.set_preconditioning_temperature",
            "0d00007e42",
        ),
        (
            C.CHARGING_LIMITS,
            {"SOC_limit": 80},
            "charging.energy.set_charge_limit",
            "0850",
        ),
        (
            C.CABIN_HVAC_DEFROST_DEFOG,
            {"level": 0},
            "comfort.cabin.set_defrost_defog",
            "0804",
        ),
        (
            C.CABIN_HVAC_DEFROST_DEFOG,
            {"level": 1},
            "comfort.cabin.set_defrost_defog",
            "0803",
        ),
    ],
)
def test_command_wire(command, params, rvm, wire):
    assert encode_control_command(command, params) == (rvm, bytes.fromhex(wire))


@pytest.mark.parametrize(
    "command,instance,device",
    [
        (C.CABIN_HVAC_LEFT_SEAT_HEAT, 5, 1),
        (C.CABIN_HVAC_RIGHT_SEAT_HEAT, 7, 1),
        (C.CABIN_HVAC_REAR_LEFT_SEAT_HEAT, 8, 1),
        (C.CABIN_HVAC_REAR_RIGHT_SEAT_HEAT, 10, 1),
        (C.CABIN_HVAC_THIRD_ROW_LEFT_SEAT_HEAT, 11, 1),
        (C.CABIN_HVAC_THIRD_ROW_RIGHT_SEAT_HEAT, 13, 1),
        (C.CABIN_HVAC_LEFT_SEAT_VENT, 5, 2),
        (C.CABIN_HVAC_RIGHT_SEAT_VENT, 7, 2),
    ],
)
@pytest.mark.parametrize("legacy,level", [(0, 0), (2, 1), (3, 2), (4, 3)])
def test_seat_wire(command, instance, device, legacy, level):
    # Varint tags: instance=08, level=10, status=18, device=20.
    wire = bytes([8, instance]) + (bytes([16, level]) if level else b"")
    wire += bytes([24, 2 if level else 1, 32, device])
    assert encode_control_command(command, {"level": legacy}) == (
        "comfort.cabin.set_cabin_surface",
        wire,
    )


@pytest.mark.parametrize(
    "level,wire",
    [
        (0, "080118012001"),
        (1, "0801100118022001"),
        (2, "0801100218022001"),
        (3, "0801100318022001"),
    ],
)
def test_steering_wire(level, wire):
    assert encode_control_command(C.CABIN_HVAC_STEERING_HEAT, {"level": level})[
        1
    ] == bytes.fromhex(wire)


@pytest.mark.parametrize(
    "command,params",
    [
        (C.CHARGING_LIMITS, {"SOC_limit": 101}),
        (C.CHARGING_LIMITS, {"SOC_limit": 80.5}),
        (C.CHARGING_LIMITS, {"SOC_limit": True}),
        (C.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": float("nan")}),
        (C.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": float("inf")}),
        (C.CABIN_HVAC_LEFT_SEAT_HEAT, {"level": 1}),
        (C.CABIN_HVAC_LEFT_SEAT_HEAT, {"level": True}),
        (C.CABIN_HVAC_STEERING_HEAT, {"level": 4}),
        (C.CABIN_HVAC_DEFROST_DEFOG, {"level": 2}),
        (C.OPEN_FRUNK, {}),
    ],
)
def test_reject_invalid_inputs(command, params):
    with pytest.raises(ValueError):
        encode_control_command(command, params)
