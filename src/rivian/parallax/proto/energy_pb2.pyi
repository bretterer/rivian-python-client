from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatteryCellType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATTERY_CELL_TYPE_UNSPECIFIED: _ClassVar[BatteryCellType]
    BATTERY_CELL_50G: _ClassVar[BatteryCellType]
    BATTERY_CELL_53G: _ClassVar[BatteryCellType]
    BATTERY_CELL_G124: _ClassVar[BatteryCellType]
    BATTERY_CELL_LG_4695: _ClassVar[BatteryCellType]

class LowVoltageHealth(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOW_VOLTAGE_HEALTH_UNSPECIFIED: _ClassVar[LowVoltageHealth]
    LOW_VOLTAGE_NORMAL: _ClassVar[LowVoltageHealth]
    LOW_VOLTAGE_LOW: _ClassVar[LowVoltageHealth]
BATTERY_CELL_TYPE_UNSPECIFIED: BatteryCellType
BATTERY_CELL_50G: BatteryCellType
BATTERY_CELL_53G: BatteryCellType
BATTERY_CELL_G124: BatteryCellType
BATTERY_CELL_LG_4695: BatteryCellType
LOW_VOLTAGE_HEALTH_UNSPECIFIED: LowVoltageHealth
LOW_VOLTAGE_NORMAL: LowVoltageHealth
LOW_VOLTAGE_LOW: LowVoltageHealth

class BatteryCharacteristics(_message.Message):
    __slots__ = ("field_1", "cell_type", "field_3", "field_4", "pack_energy", "pack_energy_copy")
    FIELD_1_FIELD_NUMBER: _ClassVar[int]
    CELL_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    FIELD_4_FIELD_NUMBER: _ClassVar[int]
    PACK_ENERGY_FIELD_NUMBER: _ClassVar[int]
    PACK_ENERGY_COPY_FIELD_NUMBER: _ClassVar[int]
    field_1: int
    cell_type: BatteryCellType
    field_3: int
    field_4: int
    pack_energy: float
    pack_energy_copy: float
    def __init__(self, field_1: _Optional[int] = ..., cell_type: _Optional[_Union[BatteryCellType, str]] = ..., field_3: _Optional[int] = ..., field_4: _Optional[int] = ..., pack_energy: _Optional[float] = ..., pack_energy_copy: _Optional[float] = ...) -> None: ...

class BatteryState(_message.Message):
    __slots__ = ("charge_state", "temperatures", "field_3", "field_4", "bms_state_raw")
    class ChargeState(_message.Message):
        __slots__ = ("soc", "pack_energy", "range")
        SOC_FIELD_NUMBER: _ClassVar[int]
        PACK_ENERGY_FIELD_NUMBER: _ClassVar[int]
        RANGE_FIELD_NUMBER: _ClassVar[int]
        soc: float
        pack_energy: float
        range: float
        def __init__(self, soc: _Optional[float] = ..., pack_energy: _Optional[float] = ..., range: _Optional[float] = ...) -> None: ...
    class Temperatures(_message.Message):
        __slots__ = ("mid", "max", "min")
        MID_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        mid: float
        max: float
        min: float
        def __init__(self, mid: _Optional[float] = ..., max: _Optional[float] = ..., min: _Optional[float] = ...) -> None: ...
    CHARGE_STATE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURES_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    FIELD_4_FIELD_NUMBER: _ClassVar[int]
    BMS_STATE_RAW_FIELD_NUMBER: _ClassVar[int]
    charge_state: BatteryState.ChargeState
    temperatures: BatteryState.Temperatures
    field_3: str
    field_4: int
    bms_state_raw: int
    def __init__(self, charge_state: _Optional[_Union[BatteryState.ChargeState, _Mapping]] = ..., temperatures: _Optional[_Union[BatteryState.Temperatures, _Mapping]] = ..., field_3: _Optional[str] = ..., field_4: _Optional[int] = ..., bms_state_raw: _Optional[int] = ...) -> None: ...

class LowVoltageBatteryState(_message.Message):
    __slots__ = ("health",)
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    health: LowVoltageHealth
    def __init__(self, health: _Optional[_Union[LowVoltageHealth, str]] = ...) -> None: ...
