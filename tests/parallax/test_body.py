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
        "closureSideBinRightNextAction": 4,  # unconfirmed name: raw value
    }


def test_locks() -> None:
    """Locked/unlocked by id; entries without a state are skipped."""
    lock = body.LocksState.Lock
    result = decode(
        "body.locks.states",
        body.LocksState(
            lock=[
                lock(id=body.LOCK_DOOR_FRONT_LEFT, state=body.LOCK_STATE_LOCKED),
                lock(id=body.LOCK_DOOR_FRONT_RIGHT, state=body.LOCK_STATE_UNLOCKED),
                lock(id=body.LOCK_DOOR_REAR_LEFT),
            ]
        ),
    )
    assert result == {
        "doorFrontLeftLocked": "locked",
        "doorFrontRightLocked": "unlocked",
    }


def test_trailer_state() -> None:
    """Trailer presence maps to its enum string."""
    result = decode(
        "body.trailer.state",
        body.TrailerState(presence=body.TRAILER_PRESENT_WITH_BRAKES),
    )
    assert result == {"trailerStatus": "trailer_present_with_brakes"}


def test_wiper_fluid_level() -> None:
    """The raw washer fluid value."""
    result = decode("body.wipers.fluid_level", body.WiperFluidLevel(field_2=1))
    assert result == {"_wiperFluidLevel": 1}
