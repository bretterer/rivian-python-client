from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PowerState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POWER_STATE_UNSPECIFIED: _ClassVar[PowerState]
    POWER_SLEEP: _ClassVar[PowerState]
    POWER_STANDBY: _ClassVar[PowerState]
    POWER_READY: _ClassVar[PowerState]
    POWER_GO: _ClassVar[PowerState]
    POWER_VEHICLE_RESET: _ClassVar[PowerState]
    POWER_OTA_UPDATE: _ClassVar[PowerState]
    POWER_SHUTDOWN: _ClassVar[PowerState]

class ActiveInterface(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE_INTERFACE_UNSPECIFIED: _ClassVar[ActiveInterface]
    ACTIVE_INTERFACE_WIFI: _ClassVar[ActiveInterface]
    ACTIVE_INTERFACE_CELLULAR: _ClassVar[ActiveInterface]

class ConnectivityLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTIVITY_LEVEL_UNSPECIFIED: _ClassVar[ConnectivityLevel]
    CONNECTIVITY_LEVEL_0: _ClassVar[ConnectivityLevel]
    CONNECTIVITY_LEVEL_1: _ClassVar[ConnectivityLevel]
    CONNECTIVITY_LEVEL_2: _ClassVar[ConnectivityLevel]
    CONNECTIVITY_LEVEL_3: _ClassVar[ConnectivityLevel]
    CONNECTIVITY_LEVEL_4: _ClassVar[ConnectivityLevel]

class WifiSecurity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIFI_SECURITY_UNSPECIFIED: _ClassVar[WifiSecurity]
    WIFI_OPEN: _ClassVar[WifiSecurity]
    WIFI_WPA_PERSONAL: _ClassVar[WifiSecurity]
    WIFI_WPA_ENTERPRISE: _ClassVar[WifiSecurity]
    WIFI_WPA2_PERSONAL: _ClassVar[WifiSecurity]
    WIFI_WPA2_ENTERPRISE: _ClassVar[WifiSecurity]
    WIFI_WPA3_PERSONAL: _ClassVar[WifiSecurity]
    WIFI_WPA3_ENTERPRISE: _ClassVar[WifiSecurity]
    WIFI_ENHANCED_OPEN: _ClassVar[WifiSecurity]

class WpaStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WPA_STATUS_UNSPECIFIED: _ClassVar[WpaStatus]
    WPA_NOT_CONNECTED: _ClassVar[WpaStatus]
    WPA_CONNECTED: _ClassVar[WpaStatus]
    WPA_SCANNING: _ClassVar[WpaStatus]
    WPA_CONNECTING: _ClassVar[WpaStatus]
    WPA_DISCONNECTING: _ClassVar[WpaStatus]
    WPA_CONNECTION_FAILED: _ClassVar[WpaStatus]
    WPA_DISABLED: _ClassVar[WpaStatus]
    WPA_SCAN_FAILURE: _ClassVar[WpaStatus]
POWER_STATE_UNSPECIFIED: PowerState
POWER_SLEEP: PowerState
POWER_STANDBY: PowerState
POWER_READY: PowerState
POWER_GO: PowerState
POWER_VEHICLE_RESET: PowerState
POWER_OTA_UPDATE: PowerState
POWER_SHUTDOWN: PowerState
ACTIVE_INTERFACE_UNSPECIFIED: ActiveInterface
ACTIVE_INTERFACE_WIFI: ActiveInterface
ACTIVE_INTERFACE_CELLULAR: ActiveInterface
CONNECTIVITY_LEVEL_UNSPECIFIED: ConnectivityLevel
CONNECTIVITY_LEVEL_0: ConnectivityLevel
CONNECTIVITY_LEVEL_1: ConnectivityLevel
CONNECTIVITY_LEVEL_2: ConnectivityLevel
CONNECTIVITY_LEVEL_3: ConnectivityLevel
CONNECTIVITY_LEVEL_4: ConnectivityLevel
WIFI_SECURITY_UNSPECIFIED: WifiSecurity
WIFI_OPEN: WifiSecurity
WIFI_WPA_PERSONAL: WifiSecurity
WIFI_WPA_ENTERPRISE: WifiSecurity
WIFI_WPA2_PERSONAL: WifiSecurity
WIFI_WPA2_ENTERPRISE: WifiSecurity
WIFI_WPA3_PERSONAL: WifiSecurity
WIFI_WPA3_ENTERPRISE: WifiSecurity
WIFI_ENHANCED_OPEN: WifiSecurity
WPA_STATUS_UNSPECIFIED: WpaStatus
WPA_NOT_CONNECTED: WpaStatus
WPA_CONNECTED: WpaStatus
WPA_SCANNING: WpaStatus
WPA_CONNECTING: WpaStatus
WPA_DISCONNECTING: WpaStatus
WPA_CONNECTION_FAILED: WpaStatus
WPA_DISABLED: WpaStatus
WPA_SCAN_FAILURE: WpaStatus

class ActiveUserProfile(_message.Message):
    __slots__ = ("active_user_profile_id",)
    ACTIVE_USER_PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
    active_user_profile_id: str
    def __init__(self, active_user_profile_id: _Optional[str] = ...) -> None: ...

class VehiclePowerState(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: PowerState
    def __init__(self, state: _Optional[_Union[PowerState, str]] = ...) -> None: ...

class VehicleWheels(_message.Message):
    __slots__ = ("wheel",)
    class Wheel(_message.Message):
        __slots__ = ("wheel_package", "tire_odometer", "saved_tire_odometer_delta", "odometer_at_last_rotation", "saved_odometer_at_last_rotation_delta", "rotation_reminder_interval", "is_installed", "updated_at", "tires", "current_odometer")
        class UpdatedAt(_message.Message):
            __slots__ = ("seconds",)
            SECONDS_FIELD_NUMBER: _ClassVar[int]
            seconds: int
            def __init__(self, seconds: _Optional[int] = ...) -> None: ...
        WHEEL_PACKAGE_FIELD_NUMBER: _ClassVar[int]
        TIRE_ODOMETER_FIELD_NUMBER: _ClassVar[int]
        SAVED_TIRE_ODOMETER_DELTA_FIELD_NUMBER: _ClassVar[int]
        ODOMETER_AT_LAST_ROTATION_FIELD_NUMBER: _ClassVar[int]
        SAVED_ODOMETER_AT_LAST_ROTATION_DELTA_FIELD_NUMBER: _ClassVar[int]
        ROTATION_REMINDER_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        IS_INSTALLED_FIELD_NUMBER: _ClassVar[int]
        UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
        TIRES_FIELD_NUMBER: _ClassVar[int]
        CURRENT_ODOMETER_FIELD_NUMBER: _ClassVar[int]
        wheel_package: int
        tire_odometer: int
        saved_tire_odometer_delta: int
        odometer_at_last_rotation: int
        saved_odometer_at_last_rotation_delta: int
        rotation_reminder_interval: int
        is_installed: bool
        updated_at: VehicleWheels.Wheel.UpdatedAt
        tires: int
        current_odometer: int
        def __init__(self, wheel_package: _Optional[int] = ..., tire_odometer: _Optional[int] = ..., saved_tire_odometer_delta: _Optional[int] = ..., odometer_at_last_rotation: _Optional[int] = ..., saved_odometer_at_last_rotation_delta: _Optional[int] = ..., rotation_reminder_interval: _Optional[int] = ..., is_installed: bool = ..., updated_at: _Optional[_Union[VehicleWheels.Wheel.UpdatedAt, _Mapping]] = ..., tires: _Optional[int] = ..., current_odometer: _Optional[int] = ...) -> None: ...
    WHEEL_FIELD_NUMBER: _ClassVar[int]
    wheel: _containers.RepeatedCompositeFieldContainer[VehicleWheels.Wheel]
    def __init__(self, wheel: _Optional[_Iterable[_Union[VehicleWheels.Wheel, _Mapping]]] = ...) -> None: ...

class NetworkState(_message.Message):
    __slots__ = ("active_interface", "interfaces", "connectivity_level", "wifi", "cellular")
    class Route(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROUTE_UNSPECIFIED: _ClassVar[NetworkState.Route]
        ROUTE_WIFI: _ClassVar[NetworkState.Route]
        ROUTE_CELLULAR_CORE: _ClassVar[NetworkState.Route]
        ROUTE_CELLULAR_MEDIA: _ClassVar[NetworkState.Route]
        ROUTE_CELLULAR_HOTSPOT: _ClassVar[NetworkState.Route]
    ROUTE_UNSPECIFIED: NetworkState.Route
    ROUTE_WIFI: NetworkState.Route
    ROUTE_CELLULAR_CORE: NetworkState.Route
    ROUTE_CELLULAR_MEDIA: NetworkState.Route
    ROUTE_CELLULAR_HOTSPOT: NetworkState.Route
    class RouteState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROUTE_STATE_UNSPECIFIED: _ClassVar[NetworkState.RouteState]
        ROUTE_STATE_DOWN: _ClassVar[NetworkState.RouteState]
        ROUTE_STATE_UP: _ClassVar[NetworkState.RouteState]
    ROUTE_STATE_UNSPECIFIED: NetworkState.RouteState
    ROUTE_STATE_DOWN: NetworkState.RouteState
    ROUTE_STATE_UP: NetworkState.RouteState
    class ConnStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONN_STATUS_UNSPECIFIED: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_CHECKING: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_SUCCESS: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_UNSTABLE: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_NO_NETWORK: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_OUT_OF_SERVICE: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_CAPTIVE_PORTAL: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_DNS_ERROR: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_DHCP_ERROR: _ClassVar[NetworkState.ConnStatus]
        CONN_STATUS_UNREACHABLE_UNKNOWN: _ClassVar[NetworkState.ConnStatus]
    CONN_STATUS_UNSPECIFIED: NetworkState.ConnStatus
    CONN_STATUS_CHECKING: NetworkState.ConnStatus
    CONN_STATUS_SUCCESS: NetworkState.ConnStatus
    CONN_STATUS_UNSTABLE: NetworkState.ConnStatus
    CONN_STATUS_NO_NETWORK: NetworkState.ConnStatus
    CONN_STATUS_OUT_OF_SERVICE: NetworkState.ConnStatus
    CONN_STATUS_CAPTIVE_PORTAL: NetworkState.ConnStatus
    CONN_STATUS_DNS_ERROR: NetworkState.ConnStatus
    CONN_STATUS_DHCP_ERROR: NetworkState.ConnStatus
    CONN_STATUS_UNREACHABLE_UNKNOWN: NetworkState.ConnStatus
    class Ternary(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TERNARY_UNSPECIFIED: _ClassVar[NetworkState.Ternary]
        TERNARY_FALSE: _ClassVar[NetworkState.Ternary]
        TERNARY_TRUE: _ClassVar[NetworkState.Ternary]
    TERNARY_UNSPECIFIED: NetworkState.Ternary
    TERNARY_FALSE: NetworkState.Ternary
    TERNARY_TRUE: NetworkState.Ternary
    class InterfaceStatus(_message.Message):
        __slots__ = ("id", "status")
        ID_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        id: NetworkState.Route
        status: NetworkState.RouteState
        def __init__(self, id: _Optional[_Union[NetworkState.Route, str]] = ..., status: _Optional[_Union[NetworkState.RouteState, str]] = ...) -> None: ...
    class Wifi(_message.Message):
        __slots__ = ("wpa_status", "conn_status", "ssid", "bssid", "mac_address", "ip_addresses", "antenna_bars", "signal", "link_speed", "freq", "bandwidth", "secure_status", "secured", "user_enabled")
        WPA_STATUS_FIELD_NUMBER: _ClassVar[int]
        CONN_STATUS_FIELD_NUMBER: _ClassVar[int]
        SSID_FIELD_NUMBER: _ClassVar[int]
        BSSID_FIELD_NUMBER: _ClassVar[int]
        MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        IP_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
        ANTENNA_BARS_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_FIELD_NUMBER: _ClassVar[int]
        LINK_SPEED_FIELD_NUMBER: _ClassVar[int]
        FREQ_FIELD_NUMBER: _ClassVar[int]
        BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
        SECURE_STATUS_FIELD_NUMBER: _ClassVar[int]
        SECURED_FIELD_NUMBER: _ClassVar[int]
        USER_ENABLED_FIELD_NUMBER: _ClassVar[int]
        wpa_status: WpaStatus
        conn_status: NetworkState.ConnStatus
        ssid: str
        bssid: str
        mac_address: str
        ip_addresses: _containers.RepeatedCompositeFieldContainer[NetworkState.IpAddress]
        antenna_bars: ConnectivityLevel
        signal: int
        link_speed: int
        freq: int
        bandwidth: int
        secure_status: WifiSecurity
        secured: NetworkState.Ternary
        user_enabled: NetworkState.Ternary
        def __init__(self, wpa_status: _Optional[_Union[WpaStatus, str]] = ..., conn_status: _Optional[_Union[NetworkState.ConnStatus, str]] = ..., ssid: _Optional[str] = ..., bssid: _Optional[str] = ..., mac_address: _Optional[str] = ..., ip_addresses: _Optional[_Iterable[_Union[NetworkState.IpAddress, _Mapping]]] = ..., antenna_bars: _Optional[_Union[ConnectivityLevel, str]] = ..., signal: _Optional[int] = ..., link_speed: _Optional[int] = ..., freq: _Optional[int] = ..., bandwidth: _Optional[int] = ..., secure_status: _Optional[_Union[WifiSecurity, str]] = ..., secured: _Optional[_Union[NetworkState.Ternary, str]] = ..., user_enabled: _Optional[_Union[NetworkState.Ternary, str]] = ...) -> None: ...
    class IpAddress(_message.Message):
        __slots__ = ("ipv4", "ipv6")
        IPV4_FIELD_NUMBER: _ClassVar[int]
        IPV6_FIELD_NUMBER: _ClassVar[int]
        ipv4: str
        ipv6: str
        def __init__(self, ipv4: _Optional[str] = ..., ipv6: _Optional[str] = ...) -> None: ...
    class Cellular(_message.Message):
        __slots__ = ("carrier", "mode", "antenna_bars", "signal_strength")
        CARRIER_FIELD_NUMBER: _ClassVar[int]
        MODE_FIELD_NUMBER: _ClassVar[int]
        ANTENNA_BARS_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_STRENGTH_FIELD_NUMBER: _ClassVar[int]
        carrier: str
        mode: str
        antenna_bars: ConnectivityLevel
        signal_strength: int
        def __init__(self, carrier: _Optional[str] = ..., mode: _Optional[str] = ..., antenna_bars: _Optional[_Union[ConnectivityLevel, str]] = ..., signal_strength: _Optional[int] = ...) -> None: ...
    ACTIVE_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    WIFI_FIELD_NUMBER: _ClassVar[int]
    CELLULAR_FIELD_NUMBER: _ClassVar[int]
    active_interface: ActiveInterface
    interfaces: _containers.RepeatedCompositeFieldContainer[NetworkState.InterfaceStatus]
    connectivity_level: ConnectivityLevel
    wifi: NetworkState.Wifi
    cellular: NetworkState.Cellular
    def __init__(self, active_interface: _Optional[_Union[ActiveInterface, str]] = ..., interfaces: _Optional[_Iterable[_Union[NetworkState.InterfaceStatus, _Mapping]]] = ..., connectivity_level: _Optional[_Union[ConnectivityLevel, str]] = ..., wifi: _Optional[_Union[NetworkState.Wifi, _Mapping]] = ..., cellular: _Optional[_Union[NetworkState.Cellular, _Mapping]] = ...) -> None: ...
