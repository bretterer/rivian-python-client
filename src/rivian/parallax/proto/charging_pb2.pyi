from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RemoteCommand(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REMOTE_COMMAND_UNSPECIFIED: _ClassVar[RemoteCommand]
    REMOTE_COMMAND_START: _ClassVar[RemoteCommand]
    REMOTE_COMMAND_STOP: _ClassVar[RemoteCommand]

class ConnectionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTION_STATE_UNSPECIFIED: _ClassVar[ConnectionState]
    CONNECTION_STATE_DISCONNECTED: _ClassVar[ConnectionState]
    CONNECTION_STATE_CONNECTED: _ClassVar[ConnectionState]

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

class ChargerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHARGER_STATUS_UNSPECIFIED: _ClassVar[ChargerStatus]
    CHARGER_STATUS_NOT_CONNECTED: _ClassVar[ChargerStatus]
    CHARGER_STATUS_CONNECTED_NO_CHARGE: _ClassVar[ChargerStatus]
    CHARGER_STATUS_CONNECTED_CHARGING: _ClassVar[ChargerStatus]
REMOTE_COMMAND_UNSPECIFIED: RemoteCommand
REMOTE_COMMAND_START: RemoteCommand
REMOTE_COMMAND_STOP: RemoteCommand
CONNECTION_STATE_UNSPECIFIED: ConnectionState
CONNECTION_STATE_DISCONNECTED: ConnectionState
CONNECTION_STATE_CONNECTED: ConnectionState
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
    def __init__(self, enabled: _Optional[bool] = ..., window: _Optional[_Union[ScheduleTimeWindow.Window, _Mapping]] = ...) -> None: ...

class SessionNotification(_message.Message):
    __slots__ = ("field1",)
    FIELD1_FIELD_NUMBER: _ClassVar[int]
    field1: int
    def __init__(self, field1: _Optional[int] = ...) -> None: ...

class SessionRemoteCommand(_message.Message):
    __slots__ = ("command",)
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: RemoteCommand
    def __init__(self, command: _Optional[_Union[RemoteCommand, str]] = ...) -> None: ...

class SocSlider(_message.Message):
    __slots__ = ("soc_limit",)
    SOC_LIMIT_FIELD_NUMBER: _ClassVar[int]
    soc_limit: int
    def __init__(self, soc_limit: _Optional[int] = ...) -> None: ...

class TripTarget(_message.Message):
    __slots__ = ("field2",)
    FIELD2_FIELD_NUMBER: _ClassVar[int]
    field2: int
    def __init__(self, field2: _Optional[int] = ...) -> None: ...

class SmartChargingSettings(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SmartChargingInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WeightedChargingForecast(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SessionStatus(_message.Message):
    __slots__ = ("connection_state", "charging_state", "is_active")
    CONNECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    CHARGING_STATE_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    connection_state: ConnectionState
    charging_state: ChargingState
    is_active: bool
    def __init__(self, connection_state: _Optional[_Union[ConnectionState, str]] = ..., charging_state: _Optional[_Union[ChargingState, str]] = ..., is_active: _Optional[bool] = ...) -> None: ...

class TimeEstimation(_message.Message):
    __slots__ = ("estimated_time_remaining",)
    ESTIMATED_TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    estimated_time_remaining: int
    def __init__(self, estimated_time_remaining: _Optional[int] = ...) -> None: ...

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
