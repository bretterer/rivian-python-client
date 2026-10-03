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

class CabinSurface(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CABIN_SURFACE_UNSPECIFIED: _ClassVar[CabinSurface]
    STEERING_WHEEL: _ClassVar[CabinSurface]
    REAR_GLASS: _ClassVar[CabinSurface]
    FRONT_GLASS: _ClassVar[CabinSurface]
    SIDEVIEW_MIRRORS: _ClassVar[CabinSurface]
    SEAT_ROW_1_LEFT: _ClassVar[CabinSurface]
    SEAT_ROW_1_MIDDLE: _ClassVar[CabinSurface]
    SEAT_ROW_1_RIGHT: _ClassVar[CabinSurface]
    SEAT_ROW_2_LEFT: _ClassVar[CabinSurface]
    SEAT_ROW_2_MIDDLE: _ClassVar[CabinSurface]
    SEAT_ROW_2_RIGHT: _ClassVar[CabinSurface]
    SEAT_ROW_3_LEFT: _ClassVar[CabinSurface]
    SEAT_ROW_3_MIDDLE: _ClassVar[CabinSurface]
    SEAT_ROW_3_RIGHT: _ClassVar[CabinSurface]
    WIPER_AREA: _ClassVar[CabinSurface]

class ConditioningType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONDITIONING_TYPE_UNSPECIFIED: _ClassVar[ConditioningType]
    CONDITIONING_HEAT: _ClassVar[ConditioningType]
    CONDITIONING_VENT: _ClassVar[ConditioningType]

class ConditioningLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONDITIONING_LEVEL_UNSPECIFIED: _ClassVar[ConditioningLevel]
    CONDITIONING_LEVEL_1: _ClassVar[ConditioningLevel]
    CONDITIONING_LEVEL_2: _ClassVar[ConditioningLevel]
    CONDITIONING_LEVEL_3: _ClassVar[ConditioningLevel]
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
CABIN_SURFACE_UNSPECIFIED: CabinSurface
STEERING_WHEEL: CabinSurface
REAR_GLASS: CabinSurface
FRONT_GLASS: CabinSurface
SIDEVIEW_MIRRORS: CabinSurface
SEAT_ROW_1_LEFT: CabinSurface
SEAT_ROW_1_MIDDLE: CabinSurface
SEAT_ROW_1_RIGHT: CabinSurface
SEAT_ROW_2_LEFT: CabinSurface
SEAT_ROW_2_MIDDLE: CabinSurface
SEAT_ROW_2_RIGHT: CabinSurface
SEAT_ROW_3_LEFT: CabinSurface
SEAT_ROW_3_MIDDLE: CabinSurface
SEAT_ROW_3_RIGHT: CabinSurface
WIPER_AREA: CabinSurface
CONDITIONING_TYPE_UNSPECIFIED: ConditioningType
CONDITIONING_HEAT: ConditioningType
CONDITIONING_VENT: ConditioningType
CONDITIONING_LEVEL_UNSPECIFIED: ConditioningLevel
CONDITIONING_LEVEL_1: ConditioningLevel
CONDITIONING_LEVEL_2: ConditioningLevel
CONDITIONING_LEVEL_3: ConditioningLevel

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
    __slots__ = ("surface",)
    class Surface(_message.Message):
        __slots__ = ("id", "type", "state")
        ID_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        id: CabinSurface
        type: ConditioningType
        state: ConditioningLevel
        def __init__(self, id: _Optional[_Union[CabinSurface, str]] = ..., type: _Optional[_Union[ConditioningType, str]] = ..., state: _Optional[_Union[ConditioningLevel, str]] = ...) -> None: ...
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    surface: _containers.RepeatedCompositeFieldContainer[SeatConditioningStatus.Surface]
    def __init__(self, surface: _Optional[_Iterable[_Union[SeatConditioningStatus.Surface, _Mapping]]] = ...) -> None: ...
