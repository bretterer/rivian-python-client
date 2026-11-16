"""Tests for the Parallax equivalents of vehicle commands."""

from __future__ import annotations

from typing import Any

import pytest

from rivian import Rivian, VehicleCommand
from rivian.exceptions import RivianBadRequestError
from rivian.parallax import encode_vehicle_command, vehicle_command_feature
from rivian.parallax.vehicle_command import _COMMANDS


@pytest.mark.parametrize(
    ("command", "params", "rvm", "payload"),
    [
        (VehicleCommand.LOCK_ALL_CLOSURES_FEEDBACK, None, "body.locks.lock", b""),
        (
            VehicleCommand.UNLOCK_ALL_CLOSURES,
            None,
            "body.locks.unlock",
            b"\x08\x01",
        ),
        (
            VehicleCommand.OPEN_ALL_WINDOWS,
            None,
            "body.closures.open",
            b"\x0a\x02\x90\x4e",
        ),
        (
            VehicleCommand.CLOSE_FRUNK,
            None,
            "body.closures.close",
            b"\x0a\x01\x05",
        ),
        (
            VehicleCommand.RELEASE_LEFT_SIDE_BIN,
            None,
            "body.closures.open",
            b"\x0a\x01\x08",
        ),
        (
            VehicleCommand.RELEASE_RIGHT_SIDE_BIN,
            None,
            "body.closures.open",
            b"\x0a\x01\x09",
        ),
        (VehicleCommand.PANIC_ON, None, "security.alarm.enable_panic", b""),
        (
            VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP,
            {"HVAC_set_temp": 21.0},
            "comfort.cabin.set_preconditioning_temperature",
            b"\x0d\x00\x00\xa8\x41",
        ),
        (
            VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP,
            {"HVAC_set_temp": 0},
            "comfort.cabin.set_preconditioning_temperature",
            b"\x0d\x00\x00\x00\x00",
        ),
        (
            VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT,
            {"level": 2},
            "comfort.cabin.set_cabin_surface",
            b"\x08\x05\x10\x01\x18\x02\x20\x01",
        ),
        (
            VehicleCommand.CABIN_HVAC_STEERING_HEAT,
            {"level": 0},
            "comfort.cabin.set_cabin_surface",
            b"\x08\x01\x18\x01\x20\x01",
        ),
        (
            VehicleCommand.CABIN_HVAC_DEFROST_DEFOG,
            {"level": 1},
            "comfort.cabin.set_defrost_defog",
            b"\x08\x03",
        ),
        (
            VehicleCommand.CABIN_HVAC_DEFROST_DEFOG,
            {"level": 0},
            "comfort.cabin.set_defrost_defog",
            b"\x08\x04",
        ),
        (
            VehicleCommand.CHARGING_LIMITS,
            {"SOC_limit": 80},
            "charging.energy.set_charge_limit",
            b"\x08\x50",
        ),
    ],
)
def test_encode(
    command: VehicleCommand,
    params: dict[str, Any] | None,
    rvm: str,
    payload: bytes,
) -> None:
    """Commands encode like the Rivian app's."""
    assert encode_vehicle_command(command, params) == (rvm, payload)


@pytest.mark.parametrize(
    ("model", "payload"),
    [
        ("R1T", b"\x0a\x01\x06"),  # tailgate
        ("r1t", b"\x0a\x01\x06"),
        ("R1S", b"\x0a\x01\x07"),  # liftgate
        ("R2", b"\x0a\x01\x07"),
    ],
)
def test_open_liftgate_unlatch_tailgate(model: str, payload: bytes) -> None:
    """Like the Rivian app, it opens an R1T's tailgate and any other liftgate."""
    assert encode_vehicle_command(
        VehicleCommand.OPEN_LIFTGATE_UNLATCH_TAILGATE, model=model
    ) == ("body.closures.open", payload)


def test_open_liftgate_unlatch_tailgate_needs_model() -> None:
    """Without the model, it's unknown which one to open."""
    with pytest.raises(RivianBadRequestError, match="model"):
        encode_vehicle_command(VehicleCommand.OPEN_LIFTGATE_UNLATCH_TAILGATE)


def test_feature() -> None:
    """Each command is sent over Parallax per its category's feature."""
    assert vehicle_command_feature(VehicleCommand.UNLOCK_ALL_CLOSURES) == "PVS_BD_CMD"
    assert vehicle_command_feature(VehicleCommand.PANIC_OFF) == "PVS_SEC_CMD"
    assert (
        vehicle_command_feature(VehicleCommand.CABIN_HVAC_LEFT_SEAT_VENT)
        == "PVS_COMF_CMD"
    )
    assert vehicle_command_feature(VehicleCommand.START_CHARGING) == "PVS_ENRG_CMD"
    # Like the app: LIFTGATE_CMD only shows the liftgate controls
    assert vehicle_command_feature(VehicleCommand.CLOSE_LIFTGATE) == "PVS_BD_CMD"
    assert (
        vehicle_command_feature(VehicleCommand.OPEN_LIFTGATE_UNLATCH_TAILGATE)
        == "PVS_BD_CMD"
    )
    assert vehicle_command_feature(VehicleCommand.RELEASE_LEFT_SIDE_BIN) == "PVS_BD_CMD"
    assert vehicle_command_feature(VehicleCommand.WAKE_VEHICLE) is None
    assert vehicle_command_feature("NOT_A_COMMAND") is None


@pytest.mark.parametrize(
    ("command", "params"),
    [
        (VehicleCommand.WAKE_VEHICLE, None),
        (VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT, {"level": 1}),
        (VehicleCommand.CABIN_HVAC_STEERING_HEAT, {"level": 4}),
    ],
)
def test_no_equivalent(command: VehicleCommand, params: dict[str, Any] | None) -> None:
    """Valid commands and levels with no Parallax equivalent are rejected."""
    Rivian.validate_vehicle_command(command, params)
    with pytest.raises(RivianBadRequestError, match="no Parallax equivalent"):
        encode_vehicle_command(command, params)


_INVALID: list[tuple[VehicleCommand, dict[str, Any] | None]] = [
    (VehicleCommand.CHARGING_LIMITS, None),
    (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 49}),
    (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 101}),
    (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": "80"}),
    (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 80.0}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 15.5}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 29.5}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": "22"}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": True}),
    (VehicleCommand.CABIN_HVAC_DEFROST_DEFOG, {}),
    (VehicleCommand.CABIN_HVAC_DEFROST_DEFOG, {"level": "0"}),
    (VehicleCommand.CABIN_HVAC_DEFROST_DEFOG, {"level": 5}),
    (VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT, {"level": 3.0}),
    (VehicleCommand.CABIN_HVAC_STEERING_HEAT, {"level": True}),
]
_VALID: list[tuple[VehicleCommand, dict[str, Any] | None]] = [
    (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 50}),
    (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 100}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 16}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 29.0}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 0}),
    (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 63.5}),
    (VehicleCommand.CABIN_HVAC_DEFROST_DEFOG, {"level": 0}),
    (VehicleCommand.CABIN_HVAC_DEFROST_DEFOG, {"level": 4}),
    (VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT, {"level": 4}),
    (VehicleCommand.CABIN_HVAC_STEERING_HEAT, {"level": 3}),
]


@pytest.mark.parametrize(("command", "params"), _INVALID)
def test_invalid_params(command: VehicleCommand, params: dict[str, Any] | None) -> None:
    """Invalid params are rejected either way of sending."""
    with pytest.raises(RivianBadRequestError, match="must include parameter"):
        Rivian.validate_vehicle_command(command, params)
    with pytest.raises(RivianBadRequestError, match="must include parameter"):
        encode_vehicle_command(command, params)


@pytest.mark.parametrize(("command", "params"), _VALID)
def test_valid_params(command: VehicleCommand, params: dict[str, Any] | None) -> None:
    """Params at the edges of their ranges are accepted either way of sending."""
    Rivian.validate_vehicle_command(command, params)
    encode_vehicle_command(command, params)


def test_validation_agrees() -> None:
    """The validator and the encoder accept the same params for every command."""
    samples = [params for _, params in _INVALID + _VALID] + [
        {"level": level} for level in range(5)
    ]
    for command in _COMMANDS:
        for params in samples:
            try:
                Rivian.validate_vehicle_command(command, params)
                valid = True
            except RivianBadRequestError:
                valid = False
            try:
                encode_vehicle_command(command, params)
                encoded = True
            except RivianBadRequestError as err:
                encoded = False
                if valid:  # only seat level 1 and steering wheel level 4
                    assert "no Parallax equivalent" in str(err), (command, params)
            if encoded:
                assert valid, (command, params)
