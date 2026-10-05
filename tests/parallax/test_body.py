"""Tests for the `body.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import body_pb2 as body

from .helpers import decode


def test_closures() -> None:
    """Closure states map by id; the charge port also reports its next action."""
    closure = body.ClosuresState.Closure
    result = decode(
        "body.closures.states",
        body.ClosuresState(
            closure=[
                closure(id=body.DOOR_FRONT_LEFT, state=body.CLOSURE_STATE_CLOSED),
                closure(id=body.FRUNK, state=body.CLOSURE_STATE_OPEN),
                closure(
                    id=body.CHARGE_PORT,
                    state=body.CLOSURE_STATE_OPENING,
                    charge_port_door_next_action=body.CHARGE_PORT_DOOR_CLOSE_ALLOWED,
                ),
                closure(id=99, state=body.CLOSURE_STATE_CLOSED),  # type: ignore[arg-type]
            ]
        ),
    )
    assert result == {  # the unknown id is skipped
        "doorFrontLeftClosed": "closed",
        "closureFrunkClosed": "open",
        "chargePortState": "opening",
        "closureChargePortDoorNextAction": "close_allowed",
    }


def test_closure_next_actions() -> None:
    """Each closure type's next action comes from its own field."""
    closure = body.ClosuresState.Closure
    result = decode(
        "body.closures.states",
        body.ClosuresState(
            closure=[
                closure(id=body.FRUNK, frunk_next_action=body.FRUNK_OPEN_ALLOWED),
                closure(
                    id=body.TAILGATE,
                    tailgate_next_action=body.TAILGATE_OPEN_NOT_AVAILABLE,
                ),
                closure(id=body.SIDE_BIN_LEFT, side_bin_next_action=body.SIDE_BIN_SNA),
                closure(
                    id=body.SIDE_BIN_RIGHT,
                    side_bin_next_action=body.SIDE_BIN_OPEN_NOT_ALLOWED_FAULTED,
                ),
            ]
        ),
    )
    assert result == {
        "closureFrunkClosed": None,
        "closureFrunkNextAction": "open_allowed",
        "closureTailgateClosed": None,
        "closureTailgateNextAction": "open_not_available",
        "closureSideBinLeftClosed": None,
        "closureSideBinLeftNextAction": "sna",
        "closureSideBinRightClosed": None,
        "closureSideBinRightNextAction": "open_not_allowed_faulted",
    }


def test_windows_group_and_liftgate() -> None:
    """The window group carries windowsNextAction only; ajar and liftgate map."""
    closure = body.ClosuresState.Closure
    result = decode(
        "body.closures.states",
        body.ClosuresState(
            closure=[
                closure(
                    id=body.GROUP_WINDOWS,
                    fault=body.CLOSURE_FAULT_NO_FAULT,
                    windows_next_action=body.WINDOWS_CLOSE_ALLOWED,
                ),
                closure(id=body.WINDOW_FRONT_LEFT, state=body.CLOSURE_STATE_OPEN),
                closure(
                    id=body.LIFTGATE,
                    state=body.CLOSURE_STATE_AJAR,
                    liftgate_next_action=body.LIFTGATE_CLOSE_ALLOWED,
                ),
            ]
        ),
    )
    assert result == {
        "windowsNextAction": "close_allowed",
        "windowFrontLeftClosed": "open",
        "closureLiftgateClosed": "ajar",
        "closureLiftgateNextAction": "close_allowed",
    }


def test_locks() -> None:
    """Lock states by id; entries without a state are skipped."""
    lock = body.LocksState.Lock
    result = decode(
        "body.locks.states",
        body.LocksState(
            lock=[
                lock(id=body.LOCK_DOOR_FRONT_LEFT, state=body.LOCK_STATE_LOCKED),
                lock(id=body.LOCK_DOOR_FRONT_RIGHT, state=body.LOCK_STATE_UNLOCKED),
                lock(id=body.LOCK_DOOR_REAR_LEFT, fault=body.LOCK_FAULT_FAULTED),
                lock(id=body.LOCK_GEAR_GUARD, state=body.LOCK_STATE_UNLOCKED),
                lock(id=body.LOCK_TAILGATE, state=body.LOCK_STATE_PARTIALLY_UNLOCKED),
            ]
        ),
    )
    assert result == {
        "doorFrontLeftLocked": "locked",
        "doorFrontRightLocked": "unlocked",
        "gearGuardLocked": "unlocked",
        "closureTailgateLocked": "partially_unlocked",
    }


def test_trailer_state() -> None:
    """Trailer presence and rear hitch status map to their enum strings."""
    result = decode(
        "body.trailer.state",
        body.TrailerState(
            presence=body.TRAILER_PRESENT_WITH_BRAKES,
            rear_hitch_status=body.REAR_HITCH_STATUS_TRAILER1,
        ),
    )
    assert result == {
        "trailerStatus": "trailer_present_with_brakes",
        "rearHitchStatus": "trailer1",
    }


def test_window_calibration() -> None:
    """Each window's calibration uses the GraphQL values."""
    window = body.WindowsState.Window
    result = decode(
        "body.windows.states",
        body.WindowsState(
            window=[
                window(
                    instance=body.WINDOW_INSTANCE_FRONT_LEFT,
                    calibration_status=body.CALIBRATION_STATUS_CALIBRATED,
                ),
                window(
                    instance=body.WINDOW_INSTANCE_REAR,
                    calibration_status=body.CALIBRATION_STATUS_NOT_CALIBRATED,
                ),
            ]
        ),
    )
    assert result == {
        "windowFrontLeftCalibrated": "Calibrated",
        "windowRearCalibrated": "Not_Calibrated",
    }


def test_wiper_fluid_level() -> None:
    """The washer fluid state; unset is None."""
    rvm = "body.wipers.fluid_level"
    result = decode(rvm, body.WiperFluidLevel(state=body.WIPER_FLUID_STATE_NORMAL))
    assert result == {"wiperFluidState": "normal"}
    assert decode(rvm) == {"wiperFluidState": None}
