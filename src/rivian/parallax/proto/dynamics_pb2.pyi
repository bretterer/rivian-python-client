from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DriveModeValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRIVE_MODE_UNSPECIFIED: _ClassVar[DriveModeValue]
    DRIVE_MODE_INIT: _ClassVar[DriveModeValue]
    DRIVE_MODE_EVERYDAY: _ClassVar[DriveModeValue]
    DRIVE_MODE_OFF_ROAD_SNOW_ICE: _ClassVar[DriveModeValue]
    DRIVE_MODE_OFF_ROAD_SPORT_AUTO: _ClassVar[DriveModeValue]
    DRIVE_MODE_OFF_ROAD_SPORT_DRIFT: _ClassVar[DriveModeValue]
    DRIVE_MODE_SPORT_LAUNCH: _ClassVar[DriveModeValue]
    DRIVE_MODE_FAULT: _ClassVar[DriveModeValue]
    DRIVE_MODE_SPORT: _ClassVar[DriveModeValue]
    DRIVE_MODE_DISTANCE: _ClassVar[DriveModeValue]
    DRIVE_MODE_TOWING: _ClassVar[DriveModeValue]
    DRIVE_MODE_OFF_ROAD_AUTO: _ClassVar[DriveModeValue]
    DRIVE_MODE_OFF_ROAD_SAND: _ClassVar[DriveModeValue]
    DRIVE_MODE_OFF_ROAD_ROCKS: _ClassVar[DriveModeValue]
    DRIVE_MODE_OFF_ROAD_MUD: _ClassVar[DriveModeValue]
    DRIVE_MODE_WINTER: _ClassVar[DriveModeValue]

class GearValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GEAR_NOT_DEFINED: _ClassVar[GearValue]
    GEAR_PARK: _ClassVar[GearValue]
    GEAR_REVERSE: _ClassVar[GearValue]
    GEAR_NEUTRAL: _ClassVar[GearValue]
    GEAR_DRIVE: _ClassVar[GearValue]

class KnownLocationValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KNOWN_LOCATION_UNSPECIFIED: _ClassVar[KnownLocationValue]
    KNOWN_LOCATION_UNKNOWN: _ClassVar[KnownLocationValue]
    KNOWN_LOCATION_HOME: _ClassVar[KnownLocationValue]
    KNOWN_LOCATION_WORK: _ClassVar[KnownLocationValue]

class RangeThreshold(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RANGE_THRESHOLD_UNSPECIFIED: _ClassVar[RangeThreshold]
    RANGE_THRESHOLD_NORMAL: _ClassVar[RangeThreshold]
    RANGE_THRESHOLD_LOW: _ClassVar[RangeThreshold]
    RANGE_THRESHOLD_RED: _ClassVar[RangeThreshold]
    RANGE_THRESHOLD_CRITICALLY_LOW: _ClassVar[RangeThreshold]

class TemperatureImpact(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEMPERATURE_IMPACT_UNSPECIFIED: _ClassVar[TemperatureImpact]
    TEMPERATURE_NORMAL_RANGE: _ClassVar[TemperatureImpact]
    TEMPERATURE_COLD_MAY_IMPACT: _ClassVar[TemperatureImpact]
    TEMPERATURE_COLD_IMPACT: _ClassVar[TemperatureImpact]

class TirePosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIRE_POSITION_UNSPECIFIED: _ClassVar[TirePosition]
    TIRE_FRONT_LEFT: _ClassVar[TirePosition]
    TIRE_FRONT_RIGHT: _ClassVar[TirePosition]
    TIRE_REAR_LEFT: _ClassVar[TirePosition]
    TIRE_REAR_RIGHT: _ClassVar[TirePosition]

class TirePressureStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIRE_PRESSURE_STATUS_UNSPECIFIED: _ClassVar[TirePressureStatus]
    TIRE_PRESSURE_STATUS_NORMAL: _ClassVar[TirePressureStatus]
    TIRE_PRESSURE_STATUS_WARNING_HARD: _ClassVar[TirePressureStatus]
    TIRE_PRESSURE_STATUS_WARNING_SOFT: _ClassVar[TirePressureStatus]
    TIRE_PRESSURE_STATUS_WARNING_PUNCTURE: _ClassVar[TirePressureStatus]

class BrakeFluidLow(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BRAKE_FLUID_LOW_SIGNAL_NOT_AVAILABLE: _ClassVar[BrakeFluidLow]
    BRAKE_FLUID_LOW_INACTIVE: _ClassVar[BrakeFluidLow]
    BRAKE_FLUID_LOW_ACTIVE: _ClassVar[BrakeFluidLow]
DRIVE_MODE_UNSPECIFIED: DriveModeValue
DRIVE_MODE_INIT: DriveModeValue
DRIVE_MODE_EVERYDAY: DriveModeValue
DRIVE_MODE_OFF_ROAD_SNOW_ICE: DriveModeValue
DRIVE_MODE_OFF_ROAD_SPORT_AUTO: DriveModeValue
DRIVE_MODE_OFF_ROAD_SPORT_DRIFT: DriveModeValue
DRIVE_MODE_SPORT_LAUNCH: DriveModeValue
DRIVE_MODE_FAULT: DriveModeValue
DRIVE_MODE_SPORT: DriveModeValue
DRIVE_MODE_DISTANCE: DriveModeValue
DRIVE_MODE_TOWING: DriveModeValue
DRIVE_MODE_OFF_ROAD_AUTO: DriveModeValue
DRIVE_MODE_OFF_ROAD_SAND: DriveModeValue
DRIVE_MODE_OFF_ROAD_ROCKS: DriveModeValue
DRIVE_MODE_OFF_ROAD_MUD: DriveModeValue
DRIVE_MODE_WINTER: DriveModeValue
GEAR_NOT_DEFINED: GearValue
GEAR_PARK: GearValue
GEAR_REVERSE: GearValue
GEAR_NEUTRAL: GearValue
GEAR_DRIVE: GearValue
KNOWN_LOCATION_UNSPECIFIED: KnownLocationValue
KNOWN_LOCATION_UNKNOWN: KnownLocationValue
KNOWN_LOCATION_HOME: KnownLocationValue
KNOWN_LOCATION_WORK: KnownLocationValue
RANGE_THRESHOLD_UNSPECIFIED: RangeThreshold
RANGE_THRESHOLD_NORMAL: RangeThreshold
RANGE_THRESHOLD_LOW: RangeThreshold
RANGE_THRESHOLD_RED: RangeThreshold
RANGE_THRESHOLD_CRITICALLY_LOW: RangeThreshold
TEMPERATURE_IMPACT_UNSPECIFIED: TemperatureImpact
TEMPERATURE_NORMAL_RANGE: TemperatureImpact
TEMPERATURE_COLD_MAY_IMPACT: TemperatureImpact
TEMPERATURE_COLD_IMPACT: TemperatureImpact
TIRE_POSITION_UNSPECIFIED: TirePosition
TIRE_FRONT_LEFT: TirePosition
TIRE_FRONT_RIGHT: TirePosition
TIRE_REAR_LEFT: TirePosition
TIRE_REAR_RIGHT: TirePosition
TIRE_PRESSURE_STATUS_UNSPECIFIED: TirePressureStatus
TIRE_PRESSURE_STATUS_NORMAL: TirePressureStatus
TIRE_PRESSURE_STATUS_WARNING_HARD: TirePressureStatus
TIRE_PRESSURE_STATUS_WARNING_SOFT: TirePressureStatus
TIRE_PRESSURE_STATUS_WARNING_PUNCTURE: TirePressureStatus
BRAKE_FLUID_LOW_SIGNAL_NOT_AVAILABLE: BrakeFluidLow
BRAKE_FLUID_LOW_INACTIVE: BrakeFluidLow
BRAKE_FLUID_LOW_ACTIVE: BrakeFluidLow

class DriveMode(_message.Message):
    __slots__ = ("mode", "limited_accel_cold", "limited_regen_cold")
    MODE_FIELD_NUMBER: _ClassVar[int]
    LIMITED_ACCEL_COLD_FIELD_NUMBER: _ClassVar[int]
    LIMITED_REGEN_COLD_FIELD_NUMBER: _ClassVar[int]
    mode: DriveModeValue
    limited_accel_cold: bool
    limited_regen_cold: bool
    def __init__(self, mode: _Optional[_Union[DriveModeValue, str]] = ..., limited_accel_cold: bool = ..., limited_regen_cold: bool = ...) -> None: ...

class Gear(_message.Message):
    __slots__ = ("gear",)
    GEAR_FIELD_NUMBER: _ClassVar[int]
    gear: GearValue
    def __init__(self, gear: _Optional[_Union[GearValue, str]] = ...) -> None: ...

class Gnss(_message.Message):
    __slots__ = ("latitude", "longitude", "altitude", "speed", "bearing", "position_horizontal_error", "position_vertical_error", "speed_error", "bearing_error", "time")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    BEARING_FIELD_NUMBER: _ClassVar[int]
    POSITION_HORIZONTAL_ERROR_FIELD_NUMBER: _ClassVar[int]
    POSITION_VERTICAL_ERROR_FIELD_NUMBER: _ClassVar[int]
    SPEED_ERROR_FIELD_NUMBER: _ClassVar[int]
    BEARING_ERROR_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    altitude: float
    speed: float
    bearing: float
    position_horizontal_error: float
    position_vertical_error: float
    speed_error: float
    bearing_error: float
    time: int
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., speed: _Optional[float] = ..., bearing: _Optional[float] = ..., position_horizontal_error: _Optional[float] = ..., position_vertical_error: _Optional[float] = ..., speed_error: _Optional[float] = ..., bearing_error: _Optional[float] = ..., time: _Optional[int] = ...) -> None: ...

class KnownLocation(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: KnownLocationValue
    def __init__(self, location: _Optional[_Union[KnownLocationValue, str]] = ...) -> None: ...

class Odometer(_message.Message):
    __slots__ = ("distance",)
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    distance: int
    def __init__(self, distance: _Optional[int] = ...) -> None: ...

class Range(_message.Message):
    __slots__ = ("distance_to_empty", "threshold", "temperature_impact")
    DISTANCE_TO_EMPTY_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_IMPACT_FIELD_NUMBER: _ClassVar[int]
    distance_to_empty: int
    threshold: RangeThreshold
    temperature_impact: TemperatureImpact
    def __init__(self, distance_to_empty: _Optional[int] = ..., threshold: _Optional[_Union[RangeThreshold, str]] = ..., temperature_impact: _Optional[_Union[TemperatureImpact, str]] = ...) -> None: ...

class TiresState(_message.Message):
    __slots__ = ("tpms_monitor_status", "tire")
    class Tire(_message.Message):
        __slots__ = ("pos", "status", "pressure", "validity", "timestamp")
        POS_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        PRESSURE_FIELD_NUMBER: _ClassVar[int]
        VALIDITY_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        pos: TirePosition
        status: TirePressureStatus
        pressure: float
        validity: int
        timestamp: int
        def __init__(self, pos: _Optional[_Union[TirePosition, str]] = ..., status: _Optional[_Union[TirePressureStatus, str]] = ..., pressure: _Optional[float] = ..., validity: _Optional[int] = ..., timestamp: _Optional[int] = ...) -> None: ...
    TPMS_MONITOR_STATUS_FIELD_NUMBER: _ClassVar[int]
    TIRE_FIELD_NUMBER: _ClassVar[int]
    tpms_monitor_status: int
    tire: _containers.RepeatedCompositeFieldContainer[TiresState.Tire]
    def __init__(self, tpms_monitor_status: _Optional[int] = ..., tire: _Optional[_Iterable[_Union[TiresState.Tire, _Mapping]]] = ...) -> None: ...

class Efficiency(_message.Message):
    __slots__ = ("efficiency", "field_2", "history")
    class History(_message.Message):
        __slots__ = ("index", "value")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        index: int
        value: int
        def __init__(self, index: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    EFFICIENCY_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    efficiency: int
    field_2: int
    history: _containers.RepeatedCompositeFieldContainer[Efficiency.History]
    def __init__(self, efficiency: _Optional[int] = ..., field_2: _Optional[int] = ..., history: _Optional[_Iterable[_Union[Efficiency.History, _Mapping]]] = ...) -> None: ...

class MassEstimate(_message.Message):
    __slots__ = ("mass",)
    MASS_FIELD_NUMBER: _ClassVar[int]
    mass: int
    def __init__(self, mass: _Optional[int] = ...) -> None: ...

class BrakeFluidLevel(_message.Message):
    __slots__ = ("fluid_low",)
    FLUID_LOW_FIELD_NUMBER: _ClassVar[int]
    fluid_low: BrakeFluidLow
    def __init__(self, fluid_low: _Optional[_Union[BrakeFluidLow, str]] = ...) -> None: ...
