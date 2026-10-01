from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PreconditioningStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRECONDITIONING_OFF: _ClassVar[PreconditioningStatus]
    PRECONDITIONING_INITIATE_1: _ClassVar[PreconditioningStatus]
    PRECONDITIONING_INITIATE_2: _ClassVar[PreconditioningStatus]
    PRECONDITIONING_ACTIVE: _ClassVar[PreconditioningStatus]
    PRECONDITIONING_PET_COMFORT: _ClassVar[PreconditioningStatus]

class ClimateHoldStatusValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIMATE_HOLD_STATUS_UNSPECIFIED: _ClassVar[ClimateHoldStatusValue]
    CLIMATE_HOLD_STATUS_UNAVAILABLE: _ClassVar[ClimateHoldStatusValue]
    CLIMATE_HOLD_STATUS_OFF: _ClassVar[ClimateHoldStatusValue]
    CLIMATE_HOLD_STATUS_ON: _ClassVar[ClimateHoldStatusValue]
    CLIMATE_HOLD_STATUS_FAULT: _ClassVar[ClimateHoldStatusValue]

class ClimateHoldAvailability(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIMATE_HOLD_AVAILABILITY_UNSPECIFIED: _ClassVar[ClimateHoldAvailability]
    CLIMATE_HOLD_AVAILABLE: _ClassVar[ClimateHoldAvailability]
    CLIMATE_HOLD_CONTROLLABLE: _ClassVar[ClimateHoldAvailability]
    CLIMATE_HOLD_UNAVAILABLE: _ClassVar[ClimateHoldAvailability]

class ClimateHoldUnavailabilityReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIMATE_HOLD_UNAVAILABILITY_UNSPECIFIED: _ClassVar[ClimateHoldUnavailabilityReason]
    CLIMATE_HOLD_UNAVAILABILITY_UNKNOWN: _ClassVar[ClimateHoldUnavailabilityReason]
    CLIMATE_HOLD_UNAVAILABILITY_LOW_SOC: _ClassVar[ClimateHoldUnavailabilityReason]

class DefrostStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEFROST_STATUS_UNSPECIFIED: _ClassVar[DefrostStatus]
    DEFROST_ACTIVE: _ClassVar[DefrostStatus]
    DEFROST_OFF: _ClassVar[DefrostStatus]

class PetModeState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PET_MODE_OFF: _ClassVar[PetModeState]
    PET_MODE_ON: _ClassVar[PetModeState]
    PET_MODE_DISABLED: _ClassVar[PetModeState]
    PET_MODE_FAULTY: _ClassVar[PetModeState]

class PetModeTemperatureStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PET_MODE_TEMPERATURE_DEFAULT: _ClassVar[PetModeTemperatureStatus]
    PET_MODE_TEMPERATURE_COLD: _ClassVar[PetModeTemperatureStatus]
    PET_MODE_TEMPERATURE_HOT: _ClassVar[PetModeTemperatureStatus]
    PET_MODE_TEMPERATURE_FAULTY: _ClassVar[PetModeTemperatureStatus]

class SeatId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEAT_ID_UNSPECIFIED: _ClassVar[SeatId]
    STEERING_WHEEL: _ClassVar[SeatId]
    SEAT_FRONT_LEFT: _ClassVar[SeatId]
    SEAT_FRONT_RIGHT: _ClassVar[SeatId]
    SEAT_REAR_LEFT: _ClassVar[SeatId]
    SEAT_REAR_RIGHT: _ClassVar[SeatId]
    SEAT_THIRD_ROW_LEFT: _ClassVar[SeatId]
    SEAT_THIRD_ROW_RIGHT: _ClassVar[SeatId]

class SeatConditioningType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEAT_CONDITIONING_TYPE_UNSPECIFIED: _ClassVar[SeatConditioningType]
    SEAT_CONDITIONING_HEAT: _ClassVar[SeatConditioningType]
    SEAT_CONDITIONING_VENT: _ClassVar[SeatConditioningType]

class SeatConditioningLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEAT_LEVEL_UNSPECIFIED: _ClassVar[SeatConditioningLevel]
    SEAT_LEVEL_1: _ClassVar[SeatConditioningLevel]
    SEAT_LEVEL_2: _ClassVar[SeatConditioningLevel]
    SEAT_LEVEL_3: _ClassVar[SeatConditioningLevel]
PRECONDITIONING_OFF: PreconditioningStatus
PRECONDITIONING_INITIATE_1: PreconditioningStatus
PRECONDITIONING_INITIATE_2: PreconditioningStatus
PRECONDITIONING_ACTIVE: PreconditioningStatus
PRECONDITIONING_PET_COMFORT: PreconditioningStatus
CLIMATE_HOLD_STATUS_UNSPECIFIED: ClimateHoldStatusValue
CLIMATE_HOLD_STATUS_UNAVAILABLE: ClimateHoldStatusValue
CLIMATE_HOLD_STATUS_OFF: ClimateHoldStatusValue
CLIMATE_HOLD_STATUS_ON: ClimateHoldStatusValue
CLIMATE_HOLD_STATUS_FAULT: ClimateHoldStatusValue
CLIMATE_HOLD_AVAILABILITY_UNSPECIFIED: ClimateHoldAvailability
CLIMATE_HOLD_AVAILABLE: ClimateHoldAvailability
CLIMATE_HOLD_CONTROLLABLE: ClimateHoldAvailability
CLIMATE_HOLD_UNAVAILABLE: ClimateHoldAvailability
CLIMATE_HOLD_UNAVAILABILITY_UNSPECIFIED: ClimateHoldUnavailabilityReason
CLIMATE_HOLD_UNAVAILABILITY_UNKNOWN: ClimateHoldUnavailabilityReason
CLIMATE_HOLD_UNAVAILABILITY_LOW_SOC: ClimateHoldUnavailabilityReason
DEFROST_STATUS_UNSPECIFIED: DefrostStatus
DEFROST_ACTIVE: DefrostStatus
DEFROST_OFF: DefrostStatus
PET_MODE_OFF: PetModeState
PET_MODE_ON: PetModeState
PET_MODE_DISABLED: PetModeState
PET_MODE_FAULTY: PetModeState
PET_MODE_TEMPERATURE_DEFAULT: PetModeTemperatureStatus
PET_MODE_TEMPERATURE_COLD: PetModeTemperatureStatus
PET_MODE_TEMPERATURE_HOT: PetModeTemperatureStatus
PET_MODE_TEMPERATURE_FAULTY: PetModeTemperatureStatus
SEAT_ID_UNSPECIFIED: SeatId
STEERING_WHEEL: SeatId
SEAT_FRONT_LEFT: SeatId
SEAT_FRONT_RIGHT: SeatId
SEAT_REAR_LEFT: SeatId
SEAT_REAR_RIGHT: SeatId
SEAT_THIRD_ROW_LEFT: SeatId
SEAT_THIRD_ROW_RIGHT: SeatId
SEAT_CONDITIONING_TYPE_UNSPECIFIED: SeatConditioningType
SEAT_CONDITIONING_HEAT: SeatConditioningType
SEAT_CONDITIONING_VENT: SeatConditioningType
SEAT_LEVEL_UNSPECIFIED: SeatConditioningLevel
SEAT_LEVEL_1: SeatConditioningLevel
SEAT_LEVEL_2: SeatConditioningLevel
SEAT_LEVEL_3: SeatConditioningLevel

class HvacSettingsStatus(_message.Message):
    __slots__ = ("target_temperature",)
    TARGET_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    target_temperature: float
    def __init__(self, target_temperature: _Optional[float] = ...) -> None: ...

class UserModesState(_message.Message):
    __slots__ = ("field4", "field7")
    FIELD4_FIELD_NUMBER: _ClassVar[int]
    FIELD7_FIELD_NUMBER: _ClassVar[int]
    field4: int
    field7: int
    def __init__(self, field4: _Optional[int] = ..., field7: _Optional[int] = ...) -> None: ...

class CabinPreconditioningStatus(_message.Message):
    __slots__ = ("status", "field_2")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    status: PreconditioningStatus
    field_2: int
    def __init__(self, status: _Optional[_Union[PreconditioningStatus, str]] = ..., field_2: _Optional[int] = ...) -> None: ...

class CabinTemperatures(_message.Message):
    __slots__ = ("interior_temperature", "driver_set_point")
    INTERIOR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    DRIVER_SET_POINT_FIELD_NUMBER: _ClassVar[int]
    interior_temperature: float
    driver_set_point: float
    def __init__(self, interior_temperature: _Optional[float] = ..., driver_set_point: _Optional[float] = ...) -> None: ...

class CabinVentilationSetting(_message.Message):
    __slots__ = ("enabled", "mode", "windows_position", "sunroof_position", "duration")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    WINDOWS_POSITION_FIELD_NUMBER: _ClassVar[int]
    SUNROOF_POSITION_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    mode: str
    windows_position: int
    sunroof_position: int
    duration: int
    def __init__(self, enabled: _Optional[bool] = ..., mode: _Optional[str] = ..., windows_position: _Optional[int] = ..., sunroof_position: _Optional[int] = ..., duration: _Optional[int] = ...) -> None: ...

class ClimateHoldSetting(_message.Message):
    __slots__ = ("duration",)
    DURATION_FIELD_NUMBER: _ClassVar[int]
    duration: int
    def __init__(self, duration: _Optional[int] = ...) -> None: ...

class ClimateHoldStatus(_message.Message):
    __slots__ = ("status", "availability", "unavailability_reason", "end_time")
    class EndTime(_message.Message):
        __slots__ = ("seconds",)
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        def __init__(self, seconds: _Optional[int] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    UNAVAILABILITY_REASON_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    status: ClimateHoldStatusValue
    availability: ClimateHoldAvailability
    unavailability_reason: ClimateHoldUnavailabilityReason
    end_time: ClimateHoldStatus.EndTime
    def __init__(self, status: _Optional[_Union[ClimateHoldStatusValue, str]] = ..., availability: _Optional[_Union[ClimateHoldAvailability, str]] = ..., unavailability_reason: _Optional[_Union[ClimateHoldUnavailabilityReason, str]] = ..., end_time: _Optional[_Union[ClimateHoldStatus.EndTime, _Mapping]] = ...) -> None: ...

class DefrostDefogStatus(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: DefrostStatus
    def __init__(self, status: _Optional[_Union[DefrostStatus, str]] = ...) -> None: ...

class PetModeStatus(_message.Message):
    __slots__ = ("status", "temperature_status")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_STATUS_FIELD_NUMBER: _ClassVar[int]
    status: PetModeState
    temperature_status: PetModeTemperatureStatus
    def __init__(self, status: _Optional[_Union[PetModeState, str]] = ..., temperature_status: _Optional[_Union[PetModeTemperatureStatus, str]] = ...) -> None: ...

class SeatConditioningStatus(_message.Message):
    __slots__ = ("seat",)
    class Seat(_message.Message):
        __slots__ = ("id", "type", "state")
        ID_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        id: SeatId
        type: SeatConditioningType
        state: SeatConditioningLevel
        def __init__(self, id: _Optional[_Union[SeatId, str]] = ..., type: _Optional[_Union[SeatConditioningType, str]] = ..., state: _Optional[_Union[SeatConditioningLevel, str]] = ...) -> None: ...
    SEAT_FIELD_NUMBER: _ClassVar[int]
    seat: _containers.RepeatedCompositeFieldContainer[SeatConditioningStatus.Seat]
    def __init__(self, seat: _Optional[_Iterable[_Union[SeatConditioningStatus.Seat, _Mapping]]] = ...) -> None: ...
