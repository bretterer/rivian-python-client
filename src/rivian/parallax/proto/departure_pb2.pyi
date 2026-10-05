from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DefogDefrostLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEFOG_DEFROST_OFF: _ClassVar[DefogDefrostLevel]
    DEFOG_DEFROST_DEFOG: _ClassVar[DefogDefrostLevel]
    DEFOG_DEFROST_DEFROST: _ClassVar[DefogDefrostLevel]

class SurfaceHeatVentLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_OFF: _ClassVar[SurfaceHeatVentLevel]
    SURFACE_HEAT_1: _ClassVar[SurfaceHeatVentLevel]
    SURFACE_HEAT_2: _ClassVar[SurfaceHeatVentLevel]
    SURFACE_HEAT_3: _ClassVar[SurfaceHeatVentLevel]
    SURFACE_VENT_1: _ClassVar[SurfaceHeatVentLevel]
    SURFACE_VENT_2: _ClassVar[SurfaceHeatVentLevel]
    SURFACE_VENT_3: _ClassVar[SurfaceHeatVentLevel]
DEFOG_DEFROST_OFF: DefogDefrostLevel
DEFOG_DEFROST_DEFOG: DefogDefrostLevel
DEFOG_DEFROST_DEFROST: DefogDefrostLevel
SURFACE_OFF: SurfaceHeatVentLevel
SURFACE_HEAT_1: SurfaceHeatVentLevel
SURFACE_HEAT_2: SurfaceHeatVentLevel
SURFACE_HEAT_3: SurfaceHeatVentLevel
SURFACE_VENT_1: SurfaceHeatVentLevel
SURFACE_VENT_2: SurfaceHeatVentLevel
SURFACE_VENT_3: SurfaceHeatVentLevel

class DepartureSchedules(_message.Message):
    __slots__ = ("schedule", "updated_at")
    class Schedule(_message.Message):
        __slots__ = ("id", "name", "is_enabled", "occurrence", "departure_settings")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
        OCCURRENCE_FIELD_NUMBER: _ClassVar[int]
        DEPARTURE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        is_enabled: bool
        occurrence: DepartureSchedules.Occurrence
        departure_settings: DepartureSchedules.DepartureSettings
        def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., is_enabled: bool = ..., occurrence: _Optional[_Union[DepartureSchedules.Occurrence, _Mapping]] = ..., departure_settings: _Optional[_Union[DepartureSchedules.DepartureSettings, _Mapping]] = ...) -> None: ...
    class Occurrence(_message.Message):
        __slots__ = ("days", "starts_at")
        DAYS_FIELD_NUMBER: _ClassVar[int]
        STARTS_AT_FIELD_NUMBER: _ClassVar[int]
        days: DepartureSchedules.Days
        starts_at: int
        def __init__(self, days: _Optional[_Union[DepartureSchedules.Days, _Mapping]] = ..., starts_at: _Optional[int] = ...) -> None: ...
    class Days(_message.Message):
        __slots__ = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        MONDAY_FIELD_NUMBER: _ClassVar[int]
        TUESDAY_FIELD_NUMBER: _ClassVar[int]
        WEDNESDAY_FIELD_NUMBER: _ClassVar[int]
        THURSDAY_FIELD_NUMBER: _ClassVar[int]
        FRIDAY_FIELD_NUMBER: _ClassVar[int]
        SATURDAY_FIELD_NUMBER: _ClassVar[int]
        SUNDAY_FIELD_NUMBER: _ClassVar[int]
        monday: bool
        tuesday: bool
        wednesday: bool
        thursday: bool
        friday: bool
        saturday: bool
        sunday: bool
        def __init__(self, monday: bool = ..., tuesday: bool = ..., wednesday: bool = ..., thursday: bool = ..., friday: bool = ..., saturday: bool = ..., sunday: bool = ...) -> None: ...
    class DepartureSettings(_message.Message):
        __slots__ = ("comfort_settings", "should_override_charge_schedule")
        COMFORT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        SHOULD_OVERRIDE_CHARGE_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
        comfort_settings: DepartureSchedules.ComfortSettings
        should_override_charge_schedule: bool
        def __init__(self, comfort_settings: _Optional[_Union[DepartureSchedules.ComfortSettings, _Mapping]] = ..., should_override_charge_schedule: bool = ...) -> None: ...
    class ComfortSettings(_message.Message):
        __slots__ = ("cabin_temperature", "front_defog_defrost", "surface_heat_vent_levels")
        CABIN_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
        FRONT_DEFOG_DEFROST_FIELD_NUMBER: _ClassVar[int]
        SURFACE_HEAT_VENT_LEVELS_FIELD_NUMBER: _ClassVar[int]
        cabin_temperature: float
        front_defog_defrost: DefogDefrostLevel
        surface_heat_vent_levels: DepartureSchedules.SurfaceHeatVentLevels
        def __init__(self, cabin_temperature: _Optional[float] = ..., front_defog_defrost: _Optional[_Union[DefogDefrostLevel, str]] = ..., surface_heat_vent_levels: _Optional[_Union[DepartureSchedules.SurfaceHeatVentLevels, _Mapping]] = ...) -> None: ...
    class SurfaceHeatVentLevels(_message.Message):
        __slots__ = ("front_left_seat", "front_right_seat", "rear_left_seat", "rear_right_seat", "steering_wheel")
        FRONT_LEFT_SEAT_FIELD_NUMBER: _ClassVar[int]
        FRONT_RIGHT_SEAT_FIELD_NUMBER: _ClassVar[int]
        REAR_LEFT_SEAT_FIELD_NUMBER: _ClassVar[int]
        REAR_RIGHT_SEAT_FIELD_NUMBER: _ClassVar[int]
        STEERING_WHEEL_FIELD_NUMBER: _ClassVar[int]
        front_left_seat: SurfaceHeatVentLevel
        front_right_seat: SurfaceHeatVentLevel
        rear_left_seat: SurfaceHeatVentLevel
        rear_right_seat: SurfaceHeatVentLevel
        steering_wheel: SurfaceHeatVentLevel
        def __init__(self, front_left_seat: _Optional[_Union[SurfaceHeatVentLevel, str]] = ..., front_right_seat: _Optional[_Union[SurfaceHeatVentLevel, str]] = ..., rear_left_seat: _Optional[_Union[SurfaceHeatVentLevel, str]] = ..., rear_right_seat: _Optional[_Union[SurfaceHeatVentLevel, str]] = ..., steering_wheel: _Optional[_Union[SurfaceHeatVentLevel, str]] = ...) -> None: ...
    class UpdatedAt(_message.Message):
        __slots__ = ("seconds", "nanos")
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        NANOS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        nanos: int
        def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    schedule: _containers.RepeatedCompositeFieldContainer[DepartureSchedules.Schedule]
    updated_at: DepartureSchedules.UpdatedAt
    def __init__(self, schedule: _Optional[_Iterable[_Union[DepartureSchedules.Schedule, _Mapping]]] = ..., updated_at: _Optional[_Union[DepartureSchedules.UpdatedAt, _Mapping]] = ...) -> None: ...
