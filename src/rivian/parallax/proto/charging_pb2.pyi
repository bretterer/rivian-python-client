from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChargerDerateStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DERATE_STATUS_NONE: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_WARM_ADAPTER: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_DC_WARM_PLUG: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_AC_WARM_PLUG: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_EVSE_DERATING: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_NEARING_TOC: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_NEAR_TOC_LFP_BATT_CALIBRATING: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_HVAC_PRIORITIZED: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_BATTERY_HEATING: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_BATTERY_COOLING: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_CELL_THERMAL_LIM_COLD_NO_CURRENT: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_CELL_THERMAL_LIM_HOT_NO_CURRENT: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_CELL_THERMAL_LIM_COLD: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_CELL_THERMAL_LIM_HOT: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_PACK_HARDWARE_THERMAL_LIM: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_HIGH_SOC_SIGMA: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_HV_BATTERY_FAULT: _ClassVar[ChargerDerateStatus]
    DERATE_STATUS_DCAC_EXPORT: _ClassVar[ChargerDerateStatus]

class FaultChime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FAULT_CHIME_NONE: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_ALL: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_DC: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_DC: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_GRADIENT_DC: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DEGRADED_DC: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_AC: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_AC: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DEGRADED_AC: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_PARTIAL_CONNECTION: _ClassVar[FaultChime]
    FAULT_CHIME_CHARGING_DISABLED_NOT_PARKED: _ClassVar[FaultChime]

class StartAvailability(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    START_AVAILABILITY_SNA: _ClassVar[StartAvailability]
    START_AVAILABILITY_FALSE: _ClassVar[StartAvailability]
    START_AVAILABILITY_TRUE: _ClassVar[StartAvailability]

class SmartChargingDay(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SMART_CHARGING_DAY_UNSPECIFIED: _ClassVar[SmartChargingDay]
    SMART_CHARGING_DAY_MONDAY: _ClassVar[SmartChargingDay]
    SMART_CHARGING_DAY_TUESDAY: _ClassVar[SmartChargingDay]
    SMART_CHARGING_DAY_WEDNESDAY: _ClassVar[SmartChargingDay]
    SMART_CHARGING_DAY_THURSDAY: _ClassVar[SmartChargingDay]
    SMART_CHARGING_DAY_FRIDAY: _ClassVar[SmartChargingDay]
    SMART_CHARGING_DAY_SATURDAY: _ClassVar[SmartChargingDay]
    SMART_CHARGING_DAY_SUNDAY: _ClassVar[SmartChargingDay]

class SmartChargingNotification(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SMART_CHARGING_NOTIFICATION_SNA: _ClassVar[SmartChargingNotification]
    SMART_CHARGING_NOTIFICATION_CHARGING_WITH_CLEAN_ENERGY: _ClassVar[SmartChargingNotification]
    SMART_CHARGING_NOTIFICATION_CHARGING_PAUSED: _ClassVar[SmartChargingNotification]
    SMART_CHARGING_NOTIFICATION_CLEAN_ENERGY_NOT_ENOUGH_TIME: _ClassVar[SmartChargingNotification]
    SMART_CHARGING_NOTIFICATION_CLEAN_ENERGY_FORECAST_UNAVAILABLE_OR_INCOMPLETE: _ClassVar[SmartChargingNotification]

class ConnectionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTION_STATE_INIT: _ClassVar[ConnectionState]
    CONNECTION_STATE_DISCONNECTED: _ClassVar[ConnectionState]
    CONNECTION_STATE_CONNECTED: _ClassVar[ConnectionState]
    CONNECTION_STATE_ERROR: _ClassVar[ConnectionState]
    CONNECTION_STATE_V2L_CONNECTED: _ClassVar[ConnectionState]

class ChargingState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHARGING_STATE_UNSPECIFIED: _ClassVar[ChargingState]
    CHARGING_READY: _ClassVar[ChargingState]
    CHARGING_CONNECTING: _ClassVar[ChargingState]
    CHARGING_ACTIVE: _ClassVar[ChargingState]
    CHARGING_COMPLETE: _ClassVar[ChargingState]
    CHARGING_SCHEDULED: _ClassVar[ChargingState]
    CHARGING_VEHICLE_ERROR: _ClassVar[ChargingState]
    CHARGING_STATION_ERROR: _ClassVar[ChargingState]
    CHARGING_USER_STOPPED: _ClassVar[ChargingState]
    CHARGING_STATION_STOPPED: _ClassVar[ChargingState]
    CHARGING_PAYMENT_ERROR: _ClassVar[ChargingState]
    CHARGING_CERT_ERROR: _ClassVar[ChargingState]
    CHARGING_TLS_ERROR: _ClassVar[ChargingState]
    CHARGING_ERROR_AC_ADAPTER_USED_ON_DC: _ClassVar[ChargingState]
    CHARGING_ERROR_DC_ADAPTER_USED_ON_AC: _ClassVar[ChargingState]
    CHARGING_ERROR_INCOMPATIBLE_CHARGER: _ClassVar[ChargingState]
    CHARGING_SD_COMPENSATION: _ClassVar[ChargingState]
    WAITING_ON_CHARGER: _ClassVar[ChargingState]
    CHARGER_NOT_READY_OR_INCOMPATIBLE: _ClassVar[ChargingState]
    CHARGING_VEHICLE_STOPPED: _ClassVar[ChargingState]
    CHARGING_PAYMENT_ERROR_START_RIVIAN_APP: _ClassVar[ChargingState]
    CHARGING_TLS_ERROR_UNKNOWN_CHARGER: _ClassVar[ChargingState]
    CHARGING_TLS_ERROR_UNEXPECTED_FAIL: _ClassVar[ChargingState]
    CHARGING_TLS_ERROR_START_RIVIAN_APP: _ClassVar[ChargingState]
    CHARGING_SMART_CHARGING_PAUSED: _ClassVar[ChargingState]
    CHARGING_SMART_CHARGING_ACTIVE: _ClassVar[ChargingState]

class TimeEstimationValidity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIME_ESTIMATION_VALIDITY_NONE: _ClassVar[TimeEstimationValidity]
    TIME_ESTIMATION_VALIDITY_VALID: _ClassVar[TimeEstimationValidity]
    TIME_ESTIMATION_VALIDITY_INVALID: _ClassVar[TimeEstimationValidity]
    TIME_ESTIMATION_VALIDITY_PACK_DISCHARGING: _ClassVar[TimeEstimationValidity]

class ChargerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHARGER_STATUS_UNSPECIFIED: _ClassVar[ChargerStatus]
    CHARGER_STATUS_NOT_CONNECTED: _ClassVar[ChargerStatus]
    CHARGER_STATUS_CONNECTED_NO_CHARGE: _ClassVar[ChargerStatus]
    CHARGER_STATUS_CONNECTED_CHARGING: _ClassVar[ChargerStatus]
DERATE_STATUS_NONE: ChargerDerateStatus
DERATE_STATUS_WARM_ADAPTER: ChargerDerateStatus
DERATE_STATUS_DC_WARM_PLUG: ChargerDerateStatus
DERATE_STATUS_AC_WARM_PLUG: ChargerDerateStatus
DERATE_STATUS_EVSE_DERATING: ChargerDerateStatus
DERATE_STATUS_NEARING_TOC: ChargerDerateStatus
DERATE_STATUS_NEAR_TOC_LFP_BATT_CALIBRATING: ChargerDerateStatus
DERATE_STATUS_HVAC_PRIORITIZED: ChargerDerateStatus
DERATE_STATUS_BATTERY_HEATING: ChargerDerateStatus
DERATE_STATUS_BATTERY_COOLING: ChargerDerateStatus
DERATE_STATUS_CELL_THERMAL_LIM_COLD_NO_CURRENT: ChargerDerateStatus
DERATE_STATUS_CELL_THERMAL_LIM_HOT_NO_CURRENT: ChargerDerateStatus
DERATE_STATUS_CELL_THERMAL_LIM_COLD: ChargerDerateStatus
DERATE_STATUS_CELL_THERMAL_LIM_HOT: ChargerDerateStatus
DERATE_STATUS_PACK_HARDWARE_THERMAL_LIM: ChargerDerateStatus
DERATE_STATUS_HIGH_SOC_SIGMA: ChargerDerateStatus
DERATE_STATUS_HV_BATTERY_FAULT: ChargerDerateStatus
DERATE_STATUS_DCAC_EXPORT: ChargerDerateStatus
FAULT_CHIME_NONE: FaultChime
FAULT_CHIME_CHARGING_DISABLED_ALL: FaultChime
FAULT_CHIME_CHARGING_DISABLED_DC: FaultChime
FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_DC: FaultChime
FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_GRADIENT_DC: FaultChime
FAULT_CHIME_CHARGING_DEGRADED_DC: FaultChime
FAULT_CHIME_CHARGING_DISABLED_AC: FaultChime
FAULT_CHIME_CHARGING_DISABLED_PIN_TEMP_AC: FaultChime
FAULT_CHIME_CHARGING_DEGRADED_AC: FaultChime
FAULT_CHIME_CHARGING_DISABLED_PARTIAL_CONNECTION: FaultChime
FAULT_CHIME_CHARGING_DISABLED_NOT_PARKED: FaultChime
START_AVAILABILITY_SNA: StartAvailability
START_AVAILABILITY_FALSE: StartAvailability
START_AVAILABILITY_TRUE: StartAvailability
SMART_CHARGING_DAY_UNSPECIFIED: SmartChargingDay
SMART_CHARGING_DAY_MONDAY: SmartChargingDay
SMART_CHARGING_DAY_TUESDAY: SmartChargingDay
SMART_CHARGING_DAY_WEDNESDAY: SmartChargingDay
SMART_CHARGING_DAY_THURSDAY: SmartChargingDay
SMART_CHARGING_DAY_FRIDAY: SmartChargingDay
SMART_CHARGING_DAY_SATURDAY: SmartChargingDay
SMART_CHARGING_DAY_SUNDAY: SmartChargingDay
SMART_CHARGING_NOTIFICATION_SNA: SmartChargingNotification
SMART_CHARGING_NOTIFICATION_CHARGING_WITH_CLEAN_ENERGY: SmartChargingNotification
SMART_CHARGING_NOTIFICATION_CHARGING_PAUSED: SmartChargingNotification
SMART_CHARGING_NOTIFICATION_CLEAN_ENERGY_NOT_ENOUGH_TIME: SmartChargingNotification
SMART_CHARGING_NOTIFICATION_CLEAN_ENERGY_FORECAST_UNAVAILABLE_OR_INCOMPLETE: SmartChargingNotification
CONNECTION_STATE_INIT: ConnectionState
CONNECTION_STATE_DISCONNECTED: ConnectionState
CONNECTION_STATE_CONNECTED: ConnectionState
CONNECTION_STATE_ERROR: ConnectionState
CONNECTION_STATE_V2L_CONNECTED: ConnectionState
CHARGING_STATE_UNSPECIFIED: ChargingState
CHARGING_READY: ChargingState
CHARGING_CONNECTING: ChargingState
CHARGING_ACTIVE: ChargingState
CHARGING_COMPLETE: ChargingState
CHARGING_SCHEDULED: ChargingState
CHARGING_VEHICLE_ERROR: ChargingState
CHARGING_STATION_ERROR: ChargingState
CHARGING_USER_STOPPED: ChargingState
CHARGING_STATION_STOPPED: ChargingState
CHARGING_PAYMENT_ERROR: ChargingState
CHARGING_CERT_ERROR: ChargingState
CHARGING_TLS_ERROR: ChargingState
CHARGING_ERROR_AC_ADAPTER_USED_ON_DC: ChargingState
CHARGING_ERROR_DC_ADAPTER_USED_ON_AC: ChargingState
CHARGING_ERROR_INCOMPATIBLE_CHARGER: ChargingState
CHARGING_SD_COMPENSATION: ChargingState
WAITING_ON_CHARGER: ChargingState
CHARGER_NOT_READY_OR_INCOMPATIBLE: ChargingState
CHARGING_VEHICLE_STOPPED: ChargingState
CHARGING_PAYMENT_ERROR_START_RIVIAN_APP: ChargingState
CHARGING_TLS_ERROR_UNKNOWN_CHARGER: ChargingState
CHARGING_TLS_ERROR_UNEXPECTED_FAIL: ChargingState
CHARGING_TLS_ERROR_START_RIVIAN_APP: ChargingState
CHARGING_SMART_CHARGING_PAUSED: ChargingState
CHARGING_SMART_CHARGING_ACTIVE: ChargingState
TIME_ESTIMATION_VALIDITY_NONE: TimeEstimationValidity
TIME_ESTIMATION_VALIDITY_VALID: TimeEstimationValidity
TIME_ESTIMATION_VALIDITY_INVALID: TimeEstimationValidity
TIME_ESTIMATION_VALIDITY_PACK_DISCHARGING: TimeEstimationValidity
CHARGER_STATUS_UNSPECIFIED: ChargerStatus
CHARGER_STATUS_NOT_CONNECTED: ChargerStatus
CHARGER_STATUS_CONNECTED_NO_CHARGE: ChargerStatus
CHARGER_STATUS_CONNECTED_CHARGING: ChargerStatus

class ScheduleTimeWindow(_message.Message):
    __slots__ = ("enabled", "window")
    class DayOfWeek(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DAY_OF_WEEK_UNSPECIFIED: _ClassVar[ScheduleTimeWindow.DayOfWeek]
        SUNDAY: _ClassVar[ScheduleTimeWindow.DayOfWeek]
        MONDAY: _ClassVar[ScheduleTimeWindow.DayOfWeek]
        TUESDAY: _ClassVar[ScheduleTimeWindow.DayOfWeek]
        WEDNESDAY: _ClassVar[ScheduleTimeWindow.DayOfWeek]
        THURSDAY: _ClassVar[ScheduleTimeWindow.DayOfWeek]
        FRIDAY: _ClassVar[ScheduleTimeWindow.DayOfWeek]
        SATURDAY: _ClassVar[ScheduleTimeWindow.DayOfWeek]
    DAY_OF_WEEK_UNSPECIFIED: ScheduleTimeWindow.DayOfWeek
    SUNDAY: ScheduleTimeWindow.DayOfWeek
    MONDAY: ScheduleTimeWindow.DayOfWeek
    TUESDAY: ScheduleTimeWindow.DayOfWeek
    WEDNESDAY: ScheduleTimeWindow.DayOfWeek
    THURSDAY: ScheduleTimeWindow.DayOfWeek
    FRIDAY: ScheduleTimeWindow.DayOfWeek
    SATURDAY: ScheduleTimeWindow.DayOfWeek
    class Window(_message.Message):
        __slots__ = ("start_time", "end_time", "duration", "amps", "location", "start_day", "end_day")
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        AMPS_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        START_DAY_FIELD_NUMBER: _ClassVar[int]
        END_DAY_FIELD_NUMBER: _ClassVar[int]
        start_time: int
        end_time: int
        duration: int
        amps: int
        location: ScheduleTimeWindow.GeoCoordinate
        start_day: ScheduleTimeWindow.DayOfWeek
        end_day: ScheduleTimeWindow.DayOfWeek
        def __init__(self, start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., duration: _Optional[int] = ..., amps: _Optional[int] = ..., location: _Optional[_Union[ScheduleTimeWindow.GeoCoordinate, _Mapping]] = ..., start_day: _Optional[_Union[ScheduleTimeWindow.DayOfWeek, str]] = ..., end_day: _Optional[_Union[ScheduleTimeWindow.DayOfWeek, str]] = ...) -> None: ...
    class GeoCoordinate(_message.Message):
        __slots__ = ("latitude", "longitude")
        LATITUDE_FIELD_NUMBER: _ClassVar[int]
        LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        latitude: float
        longitude: float
        def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    window: ScheduleTimeWindow.Window
    def __init__(self, enabled: bool = ..., window: _Optional[_Union[ScheduleTimeWindow.Window, _Mapping]] = ...) -> None: ...

class SessionNotification(_message.Message):
    __slots__ = ("unexpected_stop_reason", "derate_status", "fault_chime")
    UNEXPECTED_STOP_REASON_FIELD_NUMBER: _ClassVar[int]
    DERATE_STATUS_FIELD_NUMBER: _ClassVar[int]
    FAULT_CHIME_FIELD_NUMBER: _ClassVar[int]
    unexpected_stop_reason: int
    derate_status: ChargerDerateStatus
    fault_chime: FaultChime
    def __init__(self, unexpected_stop_reason: _Optional[int] = ..., derate_status: _Optional[_Union[ChargerDerateStatus, str]] = ..., fault_chime: _Optional[_Union[FaultChime, str]] = ...) -> None: ...

class SessionRemoteCommand(_message.Message):
    __slots__ = ("start_available",)
    START_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    start_available: StartAvailability
    def __init__(self, start_available: _Optional[_Union[StartAvailability, str]] = ...) -> None: ...

class SocSlider(_message.Message):
    __slots__ = ("soc_limit",)
    SOC_LIMIT_FIELD_NUMBER: _ClassVar[int]
    soc_limit: int
    def __init__(self, soc_limit: _Optional[int] = ...) -> None: ...

class TripTarget(_message.Message):
    __slots__ = ("soc_limit",)
    SOC_LIMIT_FIELD_NUMBER: _ClassVar[int]
    soc_limit: int
    def __init__(self, soc_limit: _Optional[int] = ...) -> None: ...

class SmartChargingSettings(_message.Message):
    __slots__ = ("ready_by_times", "clean_energy_enabled")
    class ReadyByTime(_message.Message):
        __slots__ = ("hours", "minutes", "days")
        HOURS_FIELD_NUMBER: _ClassVar[int]
        MINUTES_FIELD_NUMBER: _ClassVar[int]
        DAYS_FIELD_NUMBER: _ClassVar[int]
        hours: int
        minutes: int
        days: _containers.RepeatedScalarFieldContainer[SmartChargingDay]
        def __init__(self, hours: _Optional[int] = ..., minutes: _Optional[int] = ..., days: _Optional[_Iterable[_Union[SmartChargingDay, str]]] = ...) -> None: ...
    READY_BY_TIMES_FIELD_NUMBER: _ClassVar[int]
    CLEAN_ENERGY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ready_by_times: _containers.RepeatedCompositeFieldContainer[SmartChargingSettings.ReadyByTime]
    clean_energy_enabled: bool
    def __init__(self, ready_by_times: _Optional[_Iterable[_Union[SmartChargingSettings.ReadyByTime, _Mapping]]] = ..., clean_energy_enabled: bool = ...) -> None: ...

class SmartChargingInfo(_message.Message):
    __slots__ = ("resume_time", "notification", "schedule_type")
    class ResumeTime(_message.Message):
        __slots__ = ("seconds", "nanos")
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        NANOS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        nanos: int
        def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
    RESUME_TIME_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    resume_time: SmartChargingInfo.ResumeTime
    notification: SmartChargingNotification
    schedule_type: int
    def __init__(self, resume_time: _Optional[_Union[SmartChargingInfo.ResumeTime, _Mapping]] = ..., notification: _Optional[_Union[SmartChargingNotification, str]] = ..., schedule_type: _Optional[int] = ...) -> None: ...

class WeightedChargingForecast(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SessionStatus(_message.Message):
    __slots__ = ("connection_state", "charging_state", "evse_type")
    CONNECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    CHARGING_STATE_FIELD_NUMBER: _ClassVar[int]
    EVSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    connection_state: ConnectionState
    charging_state: ChargingState
    evse_type: int
    def __init__(self, connection_state: _Optional[_Union[ConnectionState, str]] = ..., charging_state: _Optional[_Union[ChargingState, str]] = ..., evse_type: _Optional[int] = ...) -> None: ...

class TimeEstimation(_message.Message):
    __slots__ = ("validity", "estimated_time_remaining")
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    validity: TimeEstimationValidity
    estimated_time_remaining: int
    def __init__(self, validity: _Optional[_Union[TimeEstimationValidity, str]] = ..., estimated_time_remaining: _Optional[int] = ...) -> None: ...

class EnergyState(_message.Message):
    __slots__ = ("charging_state", "charger_status", "field_3", "field_10", "connection_state")
    CHARGING_STATE_FIELD_NUMBER: _ClassVar[int]
    CHARGER_STATUS_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    FIELD_10_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    charging_state: ChargingState
    charger_status: ChargerStatus
    field_3: int
    field_10: str
    connection_state: ConnectionState
    def __init__(self, charging_state: _Optional[_Union[ChargingState, str]] = ..., charger_status: _Optional[_Union[ChargerStatus, str]] = ..., field_3: _Optional[int] = ..., field_10: _Optional[str] = ..., connection_state: _Optional[_Union[ConnectionState, str]] = ...) -> None: ...

class SessionPower(_message.Message):
    __slots__ = ("power",)
    POWER_FIELD_NUMBER: _ClassVar[int]
    power: float
    def __init__(self, power: _Optional[float] = ...) -> None: ...
