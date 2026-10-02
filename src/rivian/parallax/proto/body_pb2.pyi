from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClosureId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOSURE_ID_UNSPECIFIED: _ClassVar[ClosureId]
    DOOR_FRONT_LEFT: _ClassVar[ClosureId]
    DOOR_FRONT_RIGHT: _ClassVar[ClosureId]
    DOOR_REAR_LEFT: _ClassVar[ClosureId]
    DOOR_REAR_RIGHT: _ClassVar[ClosureId]
    FRUNK: _ClassVar[ClosureId]
    TAILGATE: _ClassVar[ClosureId]
    LIFTGATE: _ClassVar[ClosureId]
    SIDE_BIN_LEFT: _ClassVar[ClosureId]
    SIDE_BIN_RIGHT: _ClassVar[ClosureId]
    CHARGE_PORT: _ClassVar[ClosureId]
    TONNEAU: _ClassVar[ClosureId]
    WINDOW_FRONT_LEFT: _ClassVar[ClosureId]
    WINDOW_FRONT_RIGHT: _ClassVar[ClosureId]
    WINDOW_REAR_LEFT: _ClassVar[ClosureId]
    WINDOW_REAR_RIGHT: _ClassVar[ClosureId]

class ClosureStateValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOSURE_STATE_UNSPECIFIED: _ClassVar[ClosureStateValue]
    CLOSURE_STATE_OPEN: _ClassVar[ClosureStateValue]
    CLOSURE_STATE_CLOSED: _ClassVar[ClosureStateValue]
    CLOSURE_STATE_OPENING: _ClassVar[ClosureStateValue]
    CLOSURE_STATE_CLOSING: _ClassVar[ClosureStateValue]

class LockId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOCK_ID_UNSPECIFIED: _ClassVar[LockId]
    LOCK_DOOR_FRONT_LEFT: _ClassVar[LockId]
    LOCK_DOOR_FRONT_RIGHT: _ClassVar[LockId]
    LOCK_DOOR_REAR_LEFT: _ClassVar[LockId]
    LOCK_DOOR_REAR_RIGHT: _ClassVar[LockId]
    LOCK_FRUNK: _ClassVar[LockId]
    LOCK_TAILGATE: _ClassVar[LockId]
    LOCK_LIFTGATE: _ClassVar[LockId]
    LOCK_SIDE_BIN_LEFT: _ClassVar[LockId]
    LOCK_SIDE_BIN_RIGHT: _ClassVar[LockId]
    LOCK_TONNEAU: _ClassVar[LockId]

class LockStateValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOCK_STATE_UNSPECIFIED: _ClassVar[LockStateValue]
    LOCK_STATE_LOCKED: _ClassVar[LockStateValue]
    LOCK_STATE_UNLOCKED: _ClassVar[LockStateValue]

class TrailerPresence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRAILER_PRESENCE_UNSPECIFIED: _ClassVar[TrailerPresence]
    TRAILER_NOT_PRESENT: _ClassVar[TrailerPresence]
    TRAILER_PRESENT: _ClassVar[TrailerPresence]
    TRAILER_PRESENT_WITH_BRAKES: _ClassVar[TrailerPresence]
    TRAILER_INVALID: _ClassVar[TrailerPresence]

class ChargePortDoorNextAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHARGE_PORT_DOOR_SNA: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_OPEN_ALLOWED: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_OPEN_NOT_AVAILABLE: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_OPEN_NOT_ALLOWED_FAULTED: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_OPENING: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_CLOSE_ALLOWED: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_OBSTRUCTED_WHILE_OPENING_CLOSE_ALLOWED: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_OBSTRUCTED_WHILE_OPENING_OPEN_ALLOWED: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_OBSTRUCTED_WHILE_CLOSING_CLOSE_ALLOWED: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_CLOSE_NOT_AVAILABLE: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_CLOSE_NOT_ALLOWED_FAULTED: _ClassVar[ChargePortDoorNextAction]
    CHARGE_PORT_DOOR_CLOSING: _ClassVar[ChargePortDoorNextAction]

class FrunkNextAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FRUNK_SNA: _ClassVar[FrunkNextAction]
    FRUNK_OPEN_ALLOWED: _ClassVar[FrunkNextAction]
    FRUNK_CLOSE_ALLOWED: _ClassVar[FrunkNextAction]
    FRUNK_OPENING: _ClassVar[FrunkNextAction]
    FRUNK_CLOSING: _ClassVar[FrunkNextAction]
    FRUNK_OPEN_NOT_AVAILABLE: _ClassVar[FrunkNextAction]
    FRUNK_CLOSE_NOT_AVAILABLE: _ClassVar[FrunkNextAction]
    FRUNK_OPEN_NOT_ALLOWED_FAULTED: _ClassVar[FrunkNextAction]
    FRUNK_CLOSE_NOT_ALLOWED_FAULTED: _ClassVar[FrunkNextAction]
    FRUNK_OPEN_ALLOWED_NO_POWERED_OPERATION: _ClassVar[FrunkNextAction]
    FRUNK_CLOSE_NOT_ALLOWED_NO_POWERED_OPERATION: _ClassVar[FrunkNextAction]
    FRUNK_OBSTRUCTED_WHILE_OPENING_CLOSE_ALLOWED: _ClassVar[FrunkNextAction]
    FRUNK_OBSTRUCTED_WHILE_CLOSING_OPEN_ALLOWED: _ClassVar[FrunkNextAction]

class SideBinNextAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIDE_BIN_SNA: _ClassVar[SideBinNextAction]
    SIDE_BIN_OPEN_ALLOWED: _ClassVar[SideBinNextAction]
    SIDE_BIN_OPENING: _ClassVar[SideBinNextAction]
    SIDE_BIN_OPEN_NOT_AVAILABLE: _ClassVar[SideBinNextAction]
    SIDE_BIN_OPEN_NOT_ALLOWED_FAULTED: _ClassVar[SideBinNextAction]
    SIDE_BIN_STUCK_AJAR_WHILE_OPENING_OPEN_ALLOWED: _ClassVar[SideBinNextAction]
    SIDE_BIN_OPEN_ALREADY_NO_ACTION_AVAILABLE: _ClassVar[SideBinNextAction]
    SIDE_BIN_OPEN_ALLOWED_CONFIRM_VEHICLE_ANGLE: _ClassVar[SideBinNextAction]

class TailgateNextAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TAILGATE_SNA: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALLOWED: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALLOWED_TRAILER_DETECTED: _ClassVar[TailgateNextAction]
    TAILGATE_OPENING: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_NOT_AVAILABLE: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_NOT_ALLOWED_FAULTED: _ClassVar[TailgateNextAction]
    TAILGATE_STUCK_AJAR_WHILE_OPENING_OPEN_ALLOWED: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALREADY_NO_ACTION_AVAILABLE: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALLOWED_CONFIRM_VEHICLE_ANGLE: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALLOWED_OBSTACLE_DETECTED: _ClassVar[TailgateNextAction]
CLOSURE_ID_UNSPECIFIED: ClosureId
DOOR_FRONT_LEFT: ClosureId
DOOR_FRONT_RIGHT: ClosureId
DOOR_REAR_LEFT: ClosureId
DOOR_REAR_RIGHT: ClosureId
FRUNK: ClosureId
TAILGATE: ClosureId
LIFTGATE: ClosureId
SIDE_BIN_LEFT: ClosureId
SIDE_BIN_RIGHT: ClosureId
CHARGE_PORT: ClosureId
TONNEAU: ClosureId
WINDOW_FRONT_LEFT: ClosureId
WINDOW_FRONT_RIGHT: ClosureId
WINDOW_REAR_LEFT: ClosureId
WINDOW_REAR_RIGHT: ClosureId
CLOSURE_STATE_UNSPECIFIED: ClosureStateValue
CLOSURE_STATE_OPEN: ClosureStateValue
CLOSURE_STATE_CLOSED: ClosureStateValue
CLOSURE_STATE_OPENING: ClosureStateValue
CLOSURE_STATE_CLOSING: ClosureStateValue
LOCK_ID_UNSPECIFIED: LockId
LOCK_DOOR_FRONT_LEFT: LockId
LOCK_DOOR_FRONT_RIGHT: LockId
LOCK_DOOR_REAR_LEFT: LockId
LOCK_DOOR_REAR_RIGHT: LockId
LOCK_FRUNK: LockId
LOCK_TAILGATE: LockId
LOCK_LIFTGATE: LockId
LOCK_SIDE_BIN_LEFT: LockId
LOCK_SIDE_BIN_RIGHT: LockId
LOCK_TONNEAU: LockId
LOCK_STATE_UNSPECIFIED: LockStateValue
LOCK_STATE_LOCKED: LockStateValue
LOCK_STATE_UNLOCKED: LockStateValue
TRAILER_PRESENCE_UNSPECIFIED: TrailerPresence
TRAILER_NOT_PRESENT: TrailerPresence
TRAILER_PRESENT: TrailerPresence
TRAILER_PRESENT_WITH_BRAKES: TrailerPresence
TRAILER_INVALID: TrailerPresence
CHARGE_PORT_DOOR_SNA: ChargePortDoorNextAction
CHARGE_PORT_DOOR_OPEN_ALLOWED: ChargePortDoorNextAction
CHARGE_PORT_DOOR_OPEN_NOT_AVAILABLE: ChargePortDoorNextAction
CHARGE_PORT_DOOR_OPEN_NOT_ALLOWED_FAULTED: ChargePortDoorNextAction
CHARGE_PORT_DOOR_OPENING: ChargePortDoorNextAction
CHARGE_PORT_DOOR_CLOSE_ALLOWED: ChargePortDoorNextAction
CHARGE_PORT_DOOR_OBSTRUCTED_WHILE_OPENING_CLOSE_ALLOWED: ChargePortDoorNextAction
CHARGE_PORT_DOOR_OBSTRUCTED_WHILE_OPENING_OPEN_ALLOWED: ChargePortDoorNextAction
CHARGE_PORT_DOOR_OBSTRUCTED_WHILE_CLOSING_CLOSE_ALLOWED: ChargePortDoorNextAction
CHARGE_PORT_DOOR_CLOSE_NOT_AVAILABLE: ChargePortDoorNextAction
CHARGE_PORT_DOOR_CLOSE_NOT_ALLOWED_FAULTED: ChargePortDoorNextAction
CHARGE_PORT_DOOR_CLOSING: ChargePortDoorNextAction
FRUNK_SNA: FrunkNextAction
FRUNK_OPEN_ALLOWED: FrunkNextAction
FRUNK_CLOSE_ALLOWED: FrunkNextAction
FRUNK_OPENING: FrunkNextAction
FRUNK_CLOSING: FrunkNextAction
FRUNK_OPEN_NOT_AVAILABLE: FrunkNextAction
FRUNK_CLOSE_NOT_AVAILABLE: FrunkNextAction
FRUNK_OPEN_NOT_ALLOWED_FAULTED: FrunkNextAction
FRUNK_CLOSE_NOT_ALLOWED_FAULTED: FrunkNextAction
FRUNK_OPEN_ALLOWED_NO_POWERED_OPERATION: FrunkNextAction
FRUNK_CLOSE_NOT_ALLOWED_NO_POWERED_OPERATION: FrunkNextAction
FRUNK_OBSTRUCTED_WHILE_OPENING_CLOSE_ALLOWED: FrunkNextAction
FRUNK_OBSTRUCTED_WHILE_CLOSING_OPEN_ALLOWED: FrunkNextAction
SIDE_BIN_SNA: SideBinNextAction
SIDE_BIN_OPEN_ALLOWED: SideBinNextAction
SIDE_BIN_OPENING: SideBinNextAction
SIDE_BIN_OPEN_NOT_AVAILABLE: SideBinNextAction
SIDE_BIN_OPEN_NOT_ALLOWED_FAULTED: SideBinNextAction
SIDE_BIN_STUCK_AJAR_WHILE_OPENING_OPEN_ALLOWED: SideBinNextAction
SIDE_BIN_OPEN_ALREADY_NO_ACTION_AVAILABLE: SideBinNextAction
SIDE_BIN_OPEN_ALLOWED_CONFIRM_VEHICLE_ANGLE: SideBinNextAction
TAILGATE_SNA: TailgateNextAction
TAILGATE_OPEN_ALLOWED: TailgateNextAction
TAILGATE_OPEN_ALLOWED_TRAILER_DETECTED: TailgateNextAction
TAILGATE_OPENING: TailgateNextAction
TAILGATE_OPEN_NOT_AVAILABLE: TailgateNextAction
TAILGATE_OPEN_NOT_ALLOWED_FAULTED: TailgateNextAction
TAILGATE_STUCK_AJAR_WHILE_OPENING_OPEN_ALLOWED: TailgateNextAction
TAILGATE_OPEN_ALREADY_NO_ACTION_AVAILABLE: TailgateNextAction
TAILGATE_OPEN_ALLOWED_CONFIRM_VEHICLE_ANGLE: TailgateNextAction
TAILGATE_OPEN_ALLOWED_OBSTACLE_DETECTED: TailgateNextAction

class ClosuresState(_message.Message):
    __slots__ = ("closure",)
    class Closure(_message.Message):
        __slots__ = ("id", "state", "field_4", "field_5", "frunk_next_action", "side_bin_next_action", "tailgate_next_action", "charge_port_door_next_action")
        ID_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        FIELD_4_FIELD_NUMBER: _ClassVar[int]
        FIELD_5_FIELD_NUMBER: _ClassVar[int]
        FRUNK_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        SIDE_BIN_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        TAILGATE_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        CHARGE_PORT_DOOR_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        id: ClosureId
        state: ClosureStateValue
        field_4: int
        field_5: int
        frunk_next_action: FrunkNextAction
        side_bin_next_action: SideBinNextAction
        tailgate_next_action: TailgateNextAction
        charge_port_door_next_action: ChargePortDoorNextAction
        def __init__(self, id: _Optional[_Union[ClosureId, str]] = ..., state: _Optional[_Union[ClosureStateValue, str]] = ..., field_4: _Optional[int] = ..., field_5: _Optional[int] = ..., frunk_next_action: _Optional[_Union[FrunkNextAction, str]] = ..., side_bin_next_action: _Optional[_Union[SideBinNextAction, str]] = ..., tailgate_next_action: _Optional[_Union[TailgateNextAction, str]] = ..., charge_port_door_next_action: _Optional[_Union[ChargePortDoorNextAction, str]] = ...) -> None: ...
    CLOSURE_FIELD_NUMBER: _ClassVar[int]
    closure: _containers.RepeatedCompositeFieldContainer[ClosuresState.Closure]
    def __init__(self, closure: _Optional[_Iterable[_Union[ClosuresState.Closure, _Mapping]]] = ...) -> None: ...

class LocksState(_message.Message):
    __slots__ = ("lock",)
    class Lock(_message.Message):
        __slots__ = ("id", "state", "field_3")
        ID_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        FIELD_3_FIELD_NUMBER: _ClassVar[int]
        id: LockId
        state: LockStateValue
        field_3: int
        def __init__(self, id: _Optional[_Union[LockId, str]] = ..., state: _Optional[_Union[LockStateValue, str]] = ..., field_3: _Optional[int] = ...) -> None: ...
    LOCK_FIELD_NUMBER: _ClassVar[int]
    lock: _containers.RepeatedCompositeFieldContainer[LocksState.Lock]
    def __init__(self, lock: _Optional[_Iterable[_Union[LocksState.Lock, _Mapping]]] = ...) -> None: ...

class TrailerState(_message.Message):
    __slots__ = ("presence", "field_2")
    PRESENCE_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    presence: TrailerPresence
    field_2: int
    def __init__(self, presence: _Optional[_Union[TrailerPresence, str]] = ..., field_2: _Optional[int] = ...) -> None: ...

class WiperFluidLevel(_message.Message):
    __slots__ = ("field_2",)
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    field_2: int
    def __init__(self, field_2: _Optional[int] = ...) -> None: ...
