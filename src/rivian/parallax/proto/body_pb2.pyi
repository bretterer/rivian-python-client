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
    WINDOW_REAR: _ClassVar[ClosureId]
    GROUP_WINDOWS: _ClassVar[ClosureId]

class ClosureState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOSURE_STATE_UNSPECIFIED: _ClassVar[ClosureState]
    CLOSURE_STATE_OPEN: _ClassVar[ClosureState]
    CLOSURE_STATE_CLOSED: _ClassVar[ClosureState]
    CLOSURE_STATE_AJAR: _ClassVar[ClosureState]
    CLOSURE_STATE_OPENING: _ClassVar[ClosureState]
    CLOSURE_STATE_CLOSING: _ClassVar[ClosureState]

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
    LOCK_CHARGE_PORT: _ClassVar[LockId]
    LOCK_TRUNK_SECURITY: _ClassVar[LockId]
    LOCK_CENTER_CONSOLE: _ClassVar[LockId]
    LOCK_GLOVE_BOX: _ClassVar[LockId]
    LOCK_GEAR_GUARD: _ClassVar[LockId]
    LOCK_TONNEAU: _ClassVar[LockId]

class LockState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOCK_STATE_UNSPECIFIED: _ClassVar[LockState]
    LOCK_STATE_LOCKED: _ClassVar[LockState]
    LOCK_STATE_UNLOCKED: _ClassVar[LockState]
    LOCK_STATE_PARTIALLY_UNLOCKED: _ClassVar[LockState]

class LockFault(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOCK_FAULT_UNSPECIFIED: _ClassVar[LockFault]
    LOCK_FAULT_FAULTED: _ClassVar[LockFault]

class WindowInstance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WINDOW_INSTANCE_UNSPECIFIED: _ClassVar[WindowInstance]
    WINDOW_INSTANCE_FRONT_LEFT: _ClassVar[WindowInstance]
    WINDOW_INSTANCE_FRONT_RIGHT: _ClassVar[WindowInstance]
    WINDOW_INSTANCE_REAR_LEFT: _ClassVar[WindowInstance]
    WINDOW_INSTANCE_REAR_RIGHT: _ClassVar[WindowInstance]
    WINDOW_INSTANCE_REAR: _ClassVar[WindowInstance]

class CalibrationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CALIBRATION_STATUS_UNSPECIFIED: _ClassVar[CalibrationStatus]
    CALIBRATION_STATUS_CALIBRATED: _ClassVar[CalibrationStatus]
    CALIBRATION_STATUS_NOT_CALIBRATED: _ClassVar[CalibrationStatus]

class RearHitchStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REAR_HITCH_STATUS_UNSPECIFIED: _ClassVar[RearHitchStatus]
    REAR_HITCH_STATUS_NOT_PRESENT: _ClassVar[RearHitchStatus]
    REAR_HITCH_STATUS_ACCESSORY: _ClassVar[RearHitchStatus]
    REAR_HITCH_STATUS_TRAILER1: _ClassVar[RearHitchStatus]
    REAR_HITCH_STATUS_TRAILER2: _ClassVar[RearHitchStatus]
    REAR_HITCH_STATUS_TRAILER3: _ClassVar[RearHitchStatus]

class ClosureFault(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOSURE_FAULT_UNSPECIFIED: _ClassVar[ClosureFault]
    CLOSURE_FAULT_NO_FAULT: _ClassVar[ClosureFault]
    CLOSURE_FAULT_GENERAL: _ClassVar[ClosureFault]
    CLOSURE_FAULT_NO_POWERED_OPERATION: _ClassVar[ClosureFault]
    CLOSURE_FAULT_OBSTRUCTED: _ClassVar[ClosureFault]

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
    FRUNK_OPEN_ALLOWED_NO_POWER_OPERATION: _ClassVar[FrunkNextAction]
    FRUNK_CLOSE_NOT_ALLOWED_NO_POWER_OPERATION: _ClassVar[FrunkNextAction]
    FRUNK_OBSTRUCTED_OPENING_CLOSE_ALLOWED: _ClassVar[FrunkNextAction]
    FRUNK_OBSTRUCTED_CLOSING_CLOSE_ALLOWED: _ClassVar[FrunkNextAction]

class LiftgateNextAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LIFTGATE_SNA: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPEN_ALLOWED: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSE_ALLOWED: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPENING: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSING: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPEN_NOT_AVAILABLE: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSE_NOT_AVAILABLE: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPEN_NOT_ALLOWED_FAULTED: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSE_NOT_ALLOWED_FAULTED: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPEN_ALLOWED_NO_POWER_OPERATION: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSE_NOT_ALLOWED_NO_POWER_OPERATION: _ClassVar[LiftgateNextAction]
    LIFTGATE_OBSTRUCTED_OPENING_CLOSE_ALLOWED: _ClassVar[LiftgateNextAction]
    LIFTGATE_OBSTRUCTED_CLOSING_CLOSE_ALLOWED: _ClassVar[LiftgateNextAction]
    LIFTGATE_LOWER_GATE_OPEN_CLOSE_NOT_ALLOWED: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPENING_PAUSE_NOT_ALLOWED: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSING_PAUSE_NOT_ALLOWED: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPEN_ALLOWED_OBSTACLE_DETECTED: _ClassVar[LiftgateNextAction]
    LIFTGATE_OPEN_ALLOWED_TRAILER_DETECTED: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSE_ALLOWED_OBSTACLE_DETECTED: _ClassVar[LiftgateNextAction]
    LIFTGATE_CLOSE_ALLOWED_TRAILER_DETECTED: _ClassVar[LiftgateNextAction]
    LIFTGATE_PROCESSING: _ClassVar[LiftgateNextAction]

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
    TAILGATE_OPENING: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_NOT_AVAILABLE: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_NOT_ALLOWED_FAULTED: _ClassVar[TailgateNextAction]
    TAILGATE_STUCK_AJAR_WHILE_OPENING_OPEN_ALLOWED: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALREADY_NO_ACTION_AVAILABLE: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALLOWED_CONFIRM_VEHICLE_ANGLE: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALLOWED_OBSTACLE_DETECTED: _ClassVar[TailgateNextAction]
    TAILGATE_OPEN_ALLOWED_TRAILER_DETECTED: _ClassVar[TailgateNextAction]

class WindowsNextAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WINDOWS_SNA: _ClassVar[WindowsNextAction]
    WINDOWS_OPEN_ALLOWED: _ClassVar[WindowsNextAction]
    WINDOWS_CLOSE_ALLOWED: _ClassVar[WindowsNextAction]
    WINDOWS_OPENING: _ClassVar[WindowsNextAction]
    WINDOWS_CLOSING: _ClassVar[WindowsNextAction]
    WINDOWS_MOVING: _ClassVar[WindowsNextAction]
    WINDOWS_OPEN_NOT_AVAILABLE: _ClassVar[WindowsNextAction]
    WINDOWS_CLOSE_NOT_AVAILABLE: _ClassVar[WindowsNextAction]
    WINDOWS_OPEN_NOT_ALLOWED_FAULTED: _ClassVar[WindowsNextAction]
    WINDOWS_CLOSE_NOT_ALLOWED_FAULTED: _ClassVar[WindowsNextAction]
    WINDOWS_OBSTRUCTED_WHILE_CLOSING_CLOSE_ALLOWED: _ClassVar[WindowsNextAction]
    WINDOWS_CLOSE_NOT_ALLOWED_UNCALIBRATED: _ClassVar[WindowsNextAction]
    WINDOWS_OPEN_NOT_ALLOWED_UNCALIBRATED: _ClassVar[WindowsNextAction]

class WiperFluidState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIPER_FLUID_STATE_UNSPECIFIED: _ClassVar[WiperFluidState]
    WIPER_FLUID_STATE_NORMAL: _ClassVar[WiperFluidState]
    WIPER_FLUID_STATE_LOW: _ClassVar[WiperFluidState]
    WIPER_FLUID_STATE_EMPTY: _ClassVar[WiperFluidState]
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
WINDOW_REAR: ClosureId
GROUP_WINDOWS: ClosureId
CLOSURE_STATE_UNSPECIFIED: ClosureState
CLOSURE_STATE_OPEN: ClosureState
CLOSURE_STATE_CLOSED: ClosureState
CLOSURE_STATE_AJAR: ClosureState
CLOSURE_STATE_OPENING: ClosureState
CLOSURE_STATE_CLOSING: ClosureState
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
LOCK_CHARGE_PORT: LockId
LOCK_TRUNK_SECURITY: LockId
LOCK_CENTER_CONSOLE: LockId
LOCK_GLOVE_BOX: LockId
LOCK_GEAR_GUARD: LockId
LOCK_TONNEAU: LockId
LOCK_STATE_UNSPECIFIED: LockState
LOCK_STATE_LOCKED: LockState
LOCK_STATE_UNLOCKED: LockState
LOCK_STATE_PARTIALLY_UNLOCKED: LockState
LOCK_FAULT_UNSPECIFIED: LockFault
LOCK_FAULT_FAULTED: LockFault
WINDOW_INSTANCE_UNSPECIFIED: WindowInstance
WINDOW_INSTANCE_FRONT_LEFT: WindowInstance
WINDOW_INSTANCE_FRONT_RIGHT: WindowInstance
WINDOW_INSTANCE_REAR_LEFT: WindowInstance
WINDOW_INSTANCE_REAR_RIGHT: WindowInstance
WINDOW_INSTANCE_REAR: WindowInstance
CALIBRATION_STATUS_UNSPECIFIED: CalibrationStatus
CALIBRATION_STATUS_CALIBRATED: CalibrationStatus
CALIBRATION_STATUS_NOT_CALIBRATED: CalibrationStatus
REAR_HITCH_STATUS_UNSPECIFIED: RearHitchStatus
REAR_HITCH_STATUS_NOT_PRESENT: RearHitchStatus
REAR_HITCH_STATUS_ACCESSORY: RearHitchStatus
REAR_HITCH_STATUS_TRAILER1: RearHitchStatus
REAR_HITCH_STATUS_TRAILER2: RearHitchStatus
REAR_HITCH_STATUS_TRAILER3: RearHitchStatus
CLOSURE_FAULT_UNSPECIFIED: ClosureFault
CLOSURE_FAULT_NO_FAULT: ClosureFault
CLOSURE_FAULT_GENERAL: ClosureFault
CLOSURE_FAULT_NO_POWERED_OPERATION: ClosureFault
CLOSURE_FAULT_OBSTRUCTED: ClosureFault
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
FRUNK_OPEN_ALLOWED_NO_POWER_OPERATION: FrunkNextAction
FRUNK_CLOSE_NOT_ALLOWED_NO_POWER_OPERATION: FrunkNextAction
FRUNK_OBSTRUCTED_OPENING_CLOSE_ALLOWED: FrunkNextAction
FRUNK_OBSTRUCTED_CLOSING_CLOSE_ALLOWED: FrunkNextAction
LIFTGATE_SNA: LiftgateNextAction
LIFTGATE_OPEN_ALLOWED: LiftgateNextAction
LIFTGATE_CLOSE_ALLOWED: LiftgateNextAction
LIFTGATE_OPENING: LiftgateNextAction
LIFTGATE_CLOSING: LiftgateNextAction
LIFTGATE_OPEN_NOT_AVAILABLE: LiftgateNextAction
LIFTGATE_CLOSE_NOT_AVAILABLE: LiftgateNextAction
LIFTGATE_OPEN_NOT_ALLOWED_FAULTED: LiftgateNextAction
LIFTGATE_CLOSE_NOT_ALLOWED_FAULTED: LiftgateNextAction
LIFTGATE_OPEN_ALLOWED_NO_POWER_OPERATION: LiftgateNextAction
LIFTGATE_CLOSE_NOT_ALLOWED_NO_POWER_OPERATION: LiftgateNextAction
LIFTGATE_OBSTRUCTED_OPENING_CLOSE_ALLOWED: LiftgateNextAction
LIFTGATE_OBSTRUCTED_CLOSING_CLOSE_ALLOWED: LiftgateNextAction
LIFTGATE_LOWER_GATE_OPEN_CLOSE_NOT_ALLOWED: LiftgateNextAction
LIFTGATE_OPENING_PAUSE_NOT_ALLOWED: LiftgateNextAction
LIFTGATE_CLOSING_PAUSE_NOT_ALLOWED: LiftgateNextAction
LIFTGATE_OPEN_ALLOWED_OBSTACLE_DETECTED: LiftgateNextAction
LIFTGATE_OPEN_ALLOWED_TRAILER_DETECTED: LiftgateNextAction
LIFTGATE_CLOSE_ALLOWED_OBSTACLE_DETECTED: LiftgateNextAction
LIFTGATE_CLOSE_ALLOWED_TRAILER_DETECTED: LiftgateNextAction
LIFTGATE_PROCESSING: LiftgateNextAction
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
TAILGATE_OPENING: TailgateNextAction
TAILGATE_OPEN_NOT_AVAILABLE: TailgateNextAction
TAILGATE_OPEN_NOT_ALLOWED_FAULTED: TailgateNextAction
TAILGATE_STUCK_AJAR_WHILE_OPENING_OPEN_ALLOWED: TailgateNextAction
TAILGATE_OPEN_ALREADY_NO_ACTION_AVAILABLE: TailgateNextAction
TAILGATE_OPEN_ALLOWED_CONFIRM_VEHICLE_ANGLE: TailgateNextAction
TAILGATE_OPEN_ALLOWED_OBSTACLE_DETECTED: TailgateNextAction
TAILGATE_OPEN_ALLOWED_TRAILER_DETECTED: TailgateNextAction
WINDOWS_SNA: WindowsNextAction
WINDOWS_OPEN_ALLOWED: WindowsNextAction
WINDOWS_CLOSE_ALLOWED: WindowsNextAction
WINDOWS_OPENING: WindowsNextAction
WINDOWS_CLOSING: WindowsNextAction
WINDOWS_MOVING: WindowsNextAction
WINDOWS_OPEN_NOT_AVAILABLE: WindowsNextAction
WINDOWS_CLOSE_NOT_AVAILABLE: WindowsNextAction
WINDOWS_OPEN_NOT_ALLOWED_FAULTED: WindowsNextAction
WINDOWS_CLOSE_NOT_ALLOWED_FAULTED: WindowsNextAction
WINDOWS_OBSTRUCTED_WHILE_CLOSING_CLOSE_ALLOWED: WindowsNextAction
WINDOWS_CLOSE_NOT_ALLOWED_UNCALIBRATED: WindowsNextAction
WINDOWS_OPEN_NOT_ALLOWED_UNCALIBRATED: WindowsNextAction
WIPER_FLUID_STATE_UNSPECIFIED: WiperFluidState
WIPER_FLUID_STATE_NORMAL: WiperFluidState
WIPER_FLUID_STATE_LOW: WiperFluidState
WIPER_FLUID_STATE_EMPTY: WiperFluidState

class ClosuresState(_message.Message):
    __slots__ = ("closure",)
    class Closure(_message.Message):
        __slots__ = ("id", "state", "open_position_percent", "fault", "windows_next_action", "frunk_next_action", "liftgate_next_action", "side_bin_next_action", "tailgate_next_action", "charge_port_door_next_action", "tonneau_next_action")
        ID_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        OPEN_POSITION_PERCENT_FIELD_NUMBER: _ClassVar[int]
        FAULT_FIELD_NUMBER: _ClassVar[int]
        WINDOWS_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        FRUNK_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        LIFTGATE_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        SIDE_BIN_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        TAILGATE_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        CHARGE_PORT_DOOR_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        TONNEAU_NEXT_ACTION_FIELD_NUMBER: _ClassVar[int]
        id: ClosureId
        state: ClosureState
        open_position_percent: int
        fault: ClosureFault
        windows_next_action: WindowsNextAction
        frunk_next_action: FrunkNextAction
        liftgate_next_action: LiftgateNextAction
        side_bin_next_action: SideBinNextAction
        tailgate_next_action: TailgateNextAction
        charge_port_door_next_action: ChargePortDoorNextAction
        tonneau_next_action: int
        def __init__(self, id: _Optional[_Union[ClosureId, str]] = ..., state: _Optional[_Union[ClosureState, str]] = ..., open_position_percent: _Optional[int] = ..., fault: _Optional[_Union[ClosureFault, str]] = ..., windows_next_action: _Optional[_Union[WindowsNextAction, str]] = ..., frunk_next_action: _Optional[_Union[FrunkNextAction, str]] = ..., liftgate_next_action: _Optional[_Union[LiftgateNextAction, str]] = ..., side_bin_next_action: _Optional[_Union[SideBinNextAction, str]] = ..., tailgate_next_action: _Optional[_Union[TailgateNextAction, str]] = ..., charge_port_door_next_action: _Optional[_Union[ChargePortDoorNextAction, str]] = ..., tonneau_next_action: _Optional[int] = ...) -> None: ...
    CLOSURE_FIELD_NUMBER: _ClassVar[int]
    closure: _containers.RepeatedCompositeFieldContainer[ClosuresState.Closure]
    def __init__(self, closure: _Optional[_Iterable[_Union[ClosuresState.Closure, _Mapping]]] = ...) -> None: ...

class LocksState(_message.Message):
    __slots__ = ("lock",)
    class Lock(_message.Message):
        __slots__ = ("id", "state", "fault")
        ID_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        FAULT_FIELD_NUMBER: _ClassVar[int]
        id: LockId
        state: LockState
        fault: LockFault
        def __init__(self, id: _Optional[_Union[LockId, str]] = ..., state: _Optional[_Union[LockState, str]] = ..., fault: _Optional[_Union[LockFault, str]] = ...) -> None: ...
    LOCK_FIELD_NUMBER: _ClassVar[int]
    lock: _containers.RepeatedCompositeFieldContainer[LocksState.Lock]
    def __init__(self, lock: _Optional[_Iterable[_Union[LocksState.Lock, _Mapping]]] = ...) -> None: ...

class WindowsState(_message.Message):
    __slots__ = ("window",)
    class Window(_message.Message):
        __slots__ = ("instance", "calibration_status")
        INSTANCE_FIELD_NUMBER: _ClassVar[int]
        CALIBRATION_STATUS_FIELD_NUMBER: _ClassVar[int]
        instance: WindowInstance
        calibration_status: CalibrationStatus
        def __init__(self, instance: _Optional[_Union[WindowInstance, str]] = ..., calibration_status: _Optional[_Union[CalibrationStatus, str]] = ...) -> None: ...
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    window: _containers.RepeatedCompositeFieldContainer[WindowsState.Window]
    def __init__(self, window: _Optional[_Iterable[_Union[WindowsState.Window, _Mapping]]] = ...) -> None: ...

class TrailerState(_message.Message):
    __slots__ = ("presence", "rear_hitch_status")
    PRESENCE_FIELD_NUMBER: _ClassVar[int]
    REAR_HITCH_STATUS_FIELD_NUMBER: _ClassVar[int]
    presence: TrailerPresence
    rear_hitch_status: RearHitchStatus
    def __init__(self, presence: _Optional[_Union[TrailerPresence, str]] = ..., rear_hitch_status: _Optional[_Union[RearHitchStatus, str]] = ...) -> None: ...

class WiperFluidLevel(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: WiperFluidState
    def __init__(self, state: _Optional[_Union[WiperFluidState, str]] = ...) -> None: ...
