from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatteryCellChemistry(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATTERY_CELL_CHEMISTRY_UNSPECIFIED: _ClassVar[BatteryCellChemistry]
    BATTERY_CELL_CHEMISTRY_NCA: _ClassVar[BatteryCellChemistry]
    BATTERY_CELL_CHEMISTRY_LFP: _ClassVar[BatteryCellChemistry]
    BATTERY_CELL_CHEMISTRY_NMC: _ClassVar[BatteryCellChemistry]

class BatteryModuleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATTERY_MODULE_TYPE_UNSPECIFIED: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_9M: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_1M: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_8M: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_6M: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_11M: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_7M: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_3M: _ClassVar[BatteryModuleType]
    BATTERY_MODULE_TYPE_10M: _ClassVar[BatteryModuleType]

class BatteryPackCapacity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATTERY_PACK_CAPACITY_UNSPECIFIED: _ClassVar[BatteryPackCapacity]
    BATTERY_PACK_CAPACITY_135KWH: _ClassVar[BatteryPackCapacity]
    BATTERY_PACK_CAPACITY_150KWH: _ClassVar[BatteryPackCapacity]
    BATTERY_PACK_CAPACITY_100KWH: _ClassVar[BatteryPackCapacity]
    BATTERY_PACK_CAPACITY_116KWH: _ClassVar[BatteryPackCapacity]
    BATTERY_PACK_CAPACITY_108KWH: _ClassVar[BatteryPackCapacity]
    BATTERY_PACK_CAPACITY_88KWH: _ClassVar[BatteryPackCapacity]

class BatteryCellType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATTERY_CELL_TYPE_UNSPECIFIED: _ClassVar[BatteryCellType]
    BATTERY_CELL_50G: _ClassVar[BatteryCellType]
    BATTERY_CELL_53G: _ClassVar[BatteryCellType]
    BATTERY_CELL_G124: _ClassVar[BatteryCellType]
    BATTERY_CELL_LG_4695: _ClassVar[BatteryCellType]

class PowerOutputStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POWER_OUTPUT_STATUS_UNSPECIFIED: _ClassVar[PowerOutputStatus]
    POWER_OUTPUT_STATUS_NOMINAL: _ClassVar[PowerOutputStatus]
    POWER_OUTPUT_STATUS_COLD: _ClassVar[PowerOutputStatus]

class LowVoltageHealth(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOW_VOLTAGE_HEALTH_UNSPECIFIED: _ClassVar[LowVoltageHealth]
    LOW_VOLTAGE_NORMAL: _ClassVar[LowVoltageHealth]
    LOW_VOLTAGE_LOW: _ClassVar[LowVoltageHealth]
BATTERY_CELL_CHEMISTRY_UNSPECIFIED: BatteryCellChemistry
BATTERY_CELL_CHEMISTRY_NCA: BatteryCellChemistry
BATTERY_CELL_CHEMISTRY_LFP: BatteryCellChemistry
BATTERY_CELL_CHEMISTRY_NMC: BatteryCellChemistry
BATTERY_MODULE_TYPE_UNSPECIFIED: BatteryModuleType
BATTERY_MODULE_TYPE_9M: BatteryModuleType
BATTERY_MODULE_TYPE_1M: BatteryModuleType
BATTERY_MODULE_TYPE_8M: BatteryModuleType
BATTERY_MODULE_TYPE_6M: BatteryModuleType
BATTERY_MODULE_TYPE_11M: BatteryModuleType
BATTERY_MODULE_TYPE_7M: BatteryModuleType
BATTERY_MODULE_TYPE_3M: BatteryModuleType
BATTERY_MODULE_TYPE_10M: BatteryModuleType
BATTERY_PACK_CAPACITY_UNSPECIFIED: BatteryPackCapacity
BATTERY_PACK_CAPACITY_135KWH: BatteryPackCapacity
BATTERY_PACK_CAPACITY_150KWH: BatteryPackCapacity
BATTERY_PACK_CAPACITY_100KWH: BatteryPackCapacity
BATTERY_PACK_CAPACITY_116KWH: BatteryPackCapacity
BATTERY_PACK_CAPACITY_108KWH: BatteryPackCapacity
BATTERY_PACK_CAPACITY_88KWH: BatteryPackCapacity
BATTERY_CELL_TYPE_UNSPECIFIED: BatteryCellType
BATTERY_CELL_50G: BatteryCellType
BATTERY_CELL_53G: BatteryCellType
BATTERY_CELL_G124: BatteryCellType
BATTERY_CELL_LG_4695: BatteryCellType
POWER_OUTPUT_STATUS_UNSPECIFIED: PowerOutputStatus
POWER_OUTPUT_STATUS_NOMINAL: PowerOutputStatus
POWER_OUTPUT_STATUS_COLD: PowerOutputStatus
LOW_VOLTAGE_HEALTH_UNSPECIFIED: LowVoltageHealth
LOW_VOLTAGE_NORMAL: LowVoltageHealth
LOW_VOLTAGE_LOW: LowVoltageHealth

class BatteryCharacteristics(_message.Message):
    __slots__ = ("chemistry", "cell_type", "module_type", "pack_capacity", "user_total_kwh", "user_max_kwh")
    CHEMISTRY_FIELD_NUMBER: _ClassVar[int]
    CELL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PACK_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    USER_TOTAL_KWH_FIELD_NUMBER: _ClassVar[int]
    USER_MAX_KWH_FIELD_NUMBER: _ClassVar[int]
    chemistry: BatteryCellChemistry
    cell_type: BatteryCellType
    module_type: BatteryModuleType
    pack_capacity: BatteryPackCapacity
    user_total_kwh: float
    user_max_kwh: float
    def __init__(self, chemistry: _Optional[_Union[BatteryCellChemistry, str]] = ..., cell_type: _Optional[_Union[BatteryCellType, str]] = ..., module_type: _Optional[_Union[BatteryModuleType, str]] = ..., pack_capacity: _Optional[_Union[BatteryPackCapacity, str]] = ..., user_total_kwh: _Optional[float] = ..., user_max_kwh: _Optional[float] = ...) -> None: ...

class BatteryState(_message.Message):
    __slots__ = ("charge_state", "temperatures", "thermal_event", "power_output", "requires_calibration", "bms_state_raw")
    class ChargeState(_message.Message):
        __slots__ = ("soc", "pack_energy")
        SOC_FIELD_NUMBER: _ClassVar[int]
        PACK_ENERGY_FIELD_NUMBER: _ClassVar[int]
        soc: float
        pack_energy: float
        def __init__(self, soc: _Optional[float] = ..., pack_energy: _Optional[float] = ...) -> None: ...
    class Temperatures(_message.Message):
        __slots__ = ("mid", "max", "min")
        MID_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        mid: float
        max: float
        min: float
        def __init__(self, mid: _Optional[float] = ..., max: _Optional[float] = ..., min: _Optional[float] = ...) -> None: ...
    class ThermalEvent(_message.Message):
        __slots__ = ("high_voltage_battery_thermal_event", "high_voltage_battery_thermal_event_propagation")
        HIGH_VOLTAGE_BATTERY_THERMAL_EVENT_FIELD_NUMBER: _ClassVar[int]
        HIGH_VOLTAGE_BATTERY_THERMAL_EVENT_PROPAGATION_FIELD_NUMBER: _ClassVar[int]
        high_voltage_battery_thermal_event: bool
        high_voltage_battery_thermal_event_propagation: bool
        def __init__(self, high_voltage_battery_thermal_event: bool = ..., high_voltage_battery_thermal_event_propagation: bool = ...) -> None: ...
    CHARGE_STATE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURES_FIELD_NUMBER: _ClassVar[int]
    THERMAL_EVENT_FIELD_NUMBER: _ClassVar[int]
    POWER_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_CALIBRATION_FIELD_NUMBER: _ClassVar[int]
    BMS_STATE_RAW_FIELD_NUMBER: _ClassVar[int]
    charge_state: BatteryState.ChargeState
    temperatures: BatteryState.Temperatures
    thermal_event: BatteryState.ThermalEvent
    power_output: PowerOutputStatus
    requires_calibration: bool
    bms_state_raw: int
    def __init__(self, charge_state: _Optional[_Union[BatteryState.ChargeState, _Mapping]] = ..., temperatures: _Optional[_Union[BatteryState.Temperatures, _Mapping]] = ..., thermal_event: _Optional[_Union[BatteryState.ThermalEvent, _Mapping]] = ..., power_output: _Optional[_Union[PowerOutputStatus, str]] = ..., requires_calibration: bool = ..., bms_state_raw: _Optional[int] = ...) -> None: ...

class LowVoltageBatteryState(_message.Message):
    __slots__ = ("health",)
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    health: LowVoltageHealth
    def __init__(self, health: _Optional[_Union[LowVoltageHealth, str]] = ...) -> None: ...
