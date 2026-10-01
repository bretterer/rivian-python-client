from rivian.parallax.proto import charging_pb2 as _charging_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColdWeatherSoc(_message.Message):
    __slots__ = ("soc",)
    SOC_FIELD_NUMBER: _ClassVar[int]
    soc: int
    def __init__(self, soc: _Optional[int] = ...) -> None: ...

class ParkedEnergyDistributions(_message.Message):
    __slots__ = ("last_24_hours", "last_8_hours", "last_park_session")
    class EnergyDistribution(_message.Message):
        __slots__ = ("total_energy", "thermal_energy", "outlets_energy", "system_energy", "gear_guard_energy", "total_range", "thermal_range", "outlets_range", "system_range", "gear_guard_range", "duration")
        TOTAL_ENERGY_FIELD_NUMBER: _ClassVar[int]
        THERMAL_ENERGY_FIELD_NUMBER: _ClassVar[int]
        OUTLETS_ENERGY_FIELD_NUMBER: _ClassVar[int]
        SYSTEM_ENERGY_FIELD_NUMBER: _ClassVar[int]
        GEAR_GUARD_ENERGY_FIELD_NUMBER: _ClassVar[int]
        TOTAL_RANGE_FIELD_NUMBER: _ClassVar[int]
        THERMAL_RANGE_FIELD_NUMBER: _ClassVar[int]
        OUTLETS_RANGE_FIELD_NUMBER: _ClassVar[int]
        SYSTEM_RANGE_FIELD_NUMBER: _ClassVar[int]
        GEAR_GUARD_RANGE_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        total_energy: float
        thermal_energy: float
        outlets_energy: float
        system_energy: float
        gear_guard_energy: float
        total_range: float
        thermal_range: float
        outlets_range: float
        system_range: float
        gear_guard_range: float
        duration: int
        def __init__(self, total_energy: _Optional[float] = ..., thermal_energy: _Optional[float] = ..., outlets_energy: _Optional[float] = ..., system_energy: _Optional[float] = ..., gear_guard_energy: _Optional[float] = ..., total_range: _Optional[float] = ..., thermal_range: _Optional[float] = ..., outlets_range: _Optional[float] = ..., system_range: _Optional[float] = ..., gear_guard_range: _Optional[float] = ..., duration: _Optional[int] = ...) -> None: ...
    LAST_24_HOURS_FIELD_NUMBER: _ClassVar[int]
    LAST_8_HOURS_FIELD_NUMBER: _ClassVar[int]
    LAST_PARK_SESSION_FIELD_NUMBER: _ClassVar[int]
    last_24_hours: ParkedEnergyDistributions.EnergyDistribution
    last_8_hours: ParkedEnergyDistributions.EnergyDistribution
    last_park_session: ParkedEnergyDistributions.EnergyDistribution
    def __init__(self, last_24_hours: _Optional[_Union[ParkedEnergyDistributions.EnergyDistribution, _Mapping]] = ..., last_8_hours: _Optional[_Union[ParkedEnergyDistributions.EnergyDistribution, _Mapping]] = ..., last_park_session: _Optional[_Union[ParkedEnergyDistributions.EnergyDistribution, _Mapping]] = ...) -> None: ...

class ChargeSessionBreakdown(_message.Message):
    __slots__ = ("total_energy", "pack_energy", "thermal_energy", "outlets_energy", "system_energy", "active_charging_time", "time_remaining", "range_added", "power", "range_rate", "session_cost", "is_free_session", "charging_state", "timestamp")
    class Money(_message.Message):
        __slots__ = ("currency_code", "units", "nanos")
        CURRENCY_CODE_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        NANOS_FIELD_NUMBER: _ClassVar[int]
        currency_code: str
        units: int
        nanos: int
        def __init__(self, currency_code: _Optional[str] = ..., units: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
    TOTAL_ENERGY_FIELD_NUMBER: _ClassVar[int]
    PACK_ENERGY_FIELD_NUMBER: _ClassVar[int]
    THERMAL_ENERGY_FIELD_NUMBER: _ClassVar[int]
    OUTLETS_ENERGY_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_ENERGY_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CHARGING_TIME_FIELD_NUMBER: _ClassVar[int]
    TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    RANGE_ADDED_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    RANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    SESSION_COST_FIELD_NUMBER: _ClassVar[int]
    IS_FREE_SESSION_FIELD_NUMBER: _ClassVar[int]
    CHARGING_STATE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    total_energy: float
    pack_energy: float
    thermal_energy: float
    outlets_energy: float
    system_energy: float
    active_charging_time: int
    time_remaining: int
    range_added: int
    power: float
    range_rate: int
    session_cost: ChargeSessionBreakdown.Money
    is_free_session: bool
    charging_state: _charging_pb2.ChargingState
    timestamp: int
    def __init__(self, total_energy: _Optional[float] = ..., pack_energy: _Optional[float] = ..., thermal_energy: _Optional[float] = ..., outlets_energy: _Optional[float] = ..., system_energy: _Optional[float] = ..., active_charging_time: _Optional[int] = ..., time_remaining: _Optional[int] = ..., range_added: _Optional[int] = ..., power: _Optional[float] = ..., range_rate: _Optional[int] = ..., session_cost: _Optional[_Union[ChargeSessionBreakdown.Money, _Mapping]] = ..., is_free_session: _Optional[bool] = ..., charging_state: _Optional[_Union[_charging_pb2.ChargingState, str]] = ..., timestamp: _Optional[int] = ...) -> None: ...

class ChargingGraphGlobal(_message.Message):
    __slots__ = ("segment",)
    class Segment(_message.Message):
        __slots__ = ("soc", "power", "start_time", "end_time", "state", "field_7")
        SOC_FIELD_NUMBER: _ClassVar[int]
        POWER_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        FIELD_7_FIELD_NUMBER: _ClassVar[int]
        soc: int
        power: float
        start_time: int
        end_time: int
        state: _charging_pb2.ChargingState
        field_7: int
        def __init__(self, soc: _Optional[int] = ..., power: _Optional[float] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., state: _Optional[_Union[_charging_pb2.ChargingState, str]] = ..., field_7: _Optional[int] = ...) -> None: ...
    SEGMENT_FIELD_NUMBER: _ClassVar[int]
    segment: _containers.RepeatedCompositeFieldContainer[ChargingGraphGlobal.Segment]
    def __init__(self, segment: _Optional[_Iterable[_Union[ChargingGraphGlobal.Segment, _Mapping]]] = ...) -> None: ...
