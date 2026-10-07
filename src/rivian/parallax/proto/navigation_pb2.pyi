from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StopStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STOP_STATUS_STOPPING: _ClassVar[StopStatus]
    STOP_STATUS_ARRIVED: _ClassVar[StopStatus]
    STOP_STATUS_NEXT_STOP: _ClassVar[StopStatus]
    STOP_STATUS_FUTURE: _ClassVar[StopStatus]
STOP_STATUS_STOPPING: StopStatus
STOP_STATUS_ARRIVED: StopStatus
STOP_STATUS_NEXT_STOP: StopStatus
STOP_STATUS_FUTURE: StopStatus

class GeoCoordinate(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...

class GpsFix(_message.Message):
    __slots__ = ("location", "speed", "bearing", "offroad", "time", "altitude", "accuracy")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    BEARING_FIELD_NUMBER: _ClassVar[int]
    OFFROAD_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    location: GeoCoordinate
    speed: float
    bearing: float
    offroad: bool
    time: int
    altitude: float
    accuracy: float
    def __init__(self, location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., speed: _Optional[float] = ..., bearing: _Optional[float] = ..., offroad: bool = ..., time: _Optional[int] = ..., altitude: _Optional[float] = ..., accuracy: _Optional[float] = ...) -> None: ...

class TripInfo(_message.Message):
    __slots__ = ("trip_id", "origin", "trip", "route_preferences", "origin_soc", "next_waypoint_departure", "faster_route")
    class ChargeDataAccuracy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CHARGE_DATA_ACCURACY_OK: _ClassVar[TripInfo.ChargeDataAccuracy]
        CHARGE_DATA_ACCURACY_CONSUMPTION_FAILED: _ClassVar[TripInfo.ChargeDataAccuracy]
        CHARGE_DATA_ACCURACY_CHARGETIME_FAILED: _ClassVar[TripInfo.ChargeDataAccuracy]
        CHARGE_DATA_ACCURACY_BOTH_FAILED: _ClassVar[TripInfo.ChargeDataAccuracy]
    CHARGE_DATA_ACCURACY_OK: TripInfo.ChargeDataAccuracy
    CHARGE_DATA_ACCURACY_CONSUMPTION_FAILED: TripInfo.ChargeDataAccuracy
    CHARGE_DATA_ACCURACY_CHARGETIME_FAILED: TripInfo.ChargeDataAccuracy
    CHARGE_DATA_ACCURACY_BOTH_FAILED: TripInfo.ChargeDataAccuracy
    class Trip(_message.Message):
        __slots__ = ("distance", "duration", "waypoint", "leg", "soc_is_below_limit", "final_soc", "final_range", "battery_empty_location", "battery_empty_to_destination_distance", "overview_polyline", "alternative_routes", "route_index", "alternative_overlaps")
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        WAYPOINT_FIELD_NUMBER: _ClassVar[int]
        LEG_FIELD_NUMBER: _ClassVar[int]
        SOC_IS_BELOW_LIMIT_FIELD_NUMBER: _ClassVar[int]
        FINAL_SOC_FIELD_NUMBER: _ClassVar[int]
        FINAL_RANGE_FIELD_NUMBER: _ClassVar[int]
        BATTERY_EMPTY_LOCATION_FIELD_NUMBER: _ClassVar[int]
        BATTERY_EMPTY_TO_DESTINATION_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        OVERVIEW_POLYLINE_FIELD_NUMBER: _ClassVar[int]
        ALTERNATIVE_ROUTES_FIELD_NUMBER: _ClassVar[int]
        ROUTE_INDEX_FIELD_NUMBER: _ClassVar[int]
        ALTERNATIVE_OVERLAPS_FIELD_NUMBER: _ClassVar[int]
        distance: float
        duration: float
        waypoint: _containers.RepeatedCompositeFieldContainer[TripInfo.WaypointWrapper]
        leg: _containers.RepeatedCompositeFieldContainer[TripInfo.Leg]
        soc_is_below_limit: bool
        final_soc: float
        final_range: float
        battery_empty_location: GeoCoordinate
        battery_empty_to_destination_distance: float
        overview_polyline: str
        alternative_routes: _containers.RepeatedCompositeFieldContainer[TripInfo.AlternativeRoute]
        route_index: int
        alternative_overlaps: _containers.RepeatedCompositeFieldContainer[TripInfo.AlternativeOverlap]
        def __init__(self, distance: _Optional[float] = ..., duration: _Optional[float] = ..., waypoint: _Optional[_Iterable[_Union[TripInfo.WaypointWrapper, _Mapping]]] = ..., leg: _Optional[_Iterable[_Union[TripInfo.Leg, _Mapping]]] = ..., soc_is_below_limit: bool = ..., final_soc: _Optional[float] = ..., final_range: _Optional[float] = ..., battery_empty_location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., battery_empty_to_destination_distance: _Optional[float] = ..., overview_polyline: _Optional[str] = ..., alternative_routes: _Optional[_Iterable[_Union[TripInfo.AlternativeRoute, _Mapping]]] = ..., route_index: _Optional[int] = ..., alternative_overlaps: _Optional[_Iterable[_Union[TripInfo.AlternativeOverlap, _Mapping]]] = ...) -> None: ...
    class WaypointWrapper(_message.Message):
        __slots__ = ("place", "charging_stop")
        PLACE_FIELD_NUMBER: _ClassVar[int]
        CHARGING_STOP_FIELD_NUMBER: _ClassVar[int]
        place: TripInfo.Place
        charging_stop: TripInfo.ChargingStop
        def __init__(self, place: _Optional[_Union[TripInfo.Place, _Mapping]] = ..., charging_stop: _Optional[_Union[TripInfo.ChargingStop, _Mapping]] = ...) -> None: ...
    class Place(_message.Message):
        __slots__ = ("location", "snapped_location", "status", "name", "place_id", "stop_duration", "soc", "range", "arrival")
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        SNAPPED_LOCATION_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        PLACE_ID_FIELD_NUMBER: _ClassVar[int]
        STOP_DURATION_FIELD_NUMBER: _ClassVar[int]
        SOC_FIELD_NUMBER: _ClassVar[int]
        RANGE_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_FIELD_NUMBER: _ClassVar[int]
        location: GeoCoordinate
        snapped_location: GeoCoordinate
        status: StopStatus
        name: str
        place_id: str
        stop_duration: float
        soc: float
        range: float
        arrival: Timestamp
        def __init__(self, location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., snapped_location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., status: _Optional[_Union[StopStatus, str]] = ..., name: _Optional[str] = ..., place_id: _Optional[str] = ..., stop_duration: _Optional[float] = ..., soc: _Optional[float] = ..., range: _Optional[float] = ..., arrival: _Optional[_Union[Timestamp, _Mapping]] = ...) -> None: ...
    class ChargingStop(_message.Message):
        __slots__ = ("station_id", "label", "location", "charge_duration", "charge_data_accuracy", "arrival_soc", "arrival_range", "departure_soc", "departure_range", "departure_time", "arrival_time", "is_system_added", "compatible", "adapter_required", "stop_duration", "status")
        STATION_ID_FIELD_NUMBER: _ClassVar[int]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        CHARGE_DURATION_FIELD_NUMBER: _ClassVar[int]
        CHARGE_DATA_ACCURACY_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_SOC_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_RANGE_FIELD_NUMBER: _ClassVar[int]
        DEPARTURE_SOC_FIELD_NUMBER: _ClassVar[int]
        DEPARTURE_RANGE_FIELD_NUMBER: _ClassVar[int]
        DEPARTURE_TIME_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_TIME_FIELD_NUMBER: _ClassVar[int]
        IS_SYSTEM_ADDED_FIELD_NUMBER: _ClassVar[int]
        COMPATIBLE_FIELD_NUMBER: _ClassVar[int]
        ADAPTER_REQUIRED_FIELD_NUMBER: _ClassVar[int]
        STOP_DURATION_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        station_id: str
        label: str
        location: GeoCoordinate
        charge_duration: float
        charge_data_accuracy: TripInfo.ChargeDataAccuracy
        arrival_soc: float
        arrival_range: float
        departure_soc: float
        departure_range: float
        departure_time: Timestamp
        arrival_time: Timestamp
        is_system_added: bool
        compatible: bool
        adapter_required: bool
        stop_duration: float
        status: StopStatus
        def __init__(self, station_id: _Optional[str] = ..., label: _Optional[str] = ..., location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., charge_duration: _Optional[float] = ..., charge_data_accuracy: _Optional[_Union[TripInfo.ChargeDataAccuracy, str]] = ..., arrival_soc: _Optional[float] = ..., arrival_range: _Optional[float] = ..., departure_soc: _Optional[float] = ..., departure_range: _Optional[float] = ..., departure_time: _Optional[_Union[Timestamp, _Mapping]] = ..., arrival_time: _Optional[_Union[Timestamp, _Mapping]] = ..., is_system_added: bool = ..., compatible: bool = ..., adapter_required: bool = ..., stop_duration: _Optional[float] = ..., status: _Optional[_Union[StopStatus, str]] = ...) -> None: ...
    class Leg(_message.Message):
        __slots__ = ("distance", "duration", "road_label", "polyline", "traffic_slow", "traffic_jam", "traffic_severe", "energy", "incidents", "traffic_blocks")
        class IncidentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            INCIDENT_UNKNOWN: _ClassVar[TripInfo.Leg.IncidentType]
            INCIDENT_NONE: _ClassVar[TripInfo.Leg.IncidentType]
            INCIDENT_CLOSURE: _ClassVar[TripInfo.Leg.IncidentType]
            INCIDENT_CRASH: _ClassVar[TripInfo.Leg.IncidentType]
            INCIDENT_CONSTRUCTION: _ClassVar[TripInfo.Leg.IncidentType]
            INCIDENT_JAM: _ClassVar[TripInfo.Leg.IncidentType]
            INCIDENT_POLICE_PRESENCE: _ClassVar[TripInfo.Leg.IncidentType]
            INCIDENT_FIXED_SPEED_CAMERA: _ClassVar[TripInfo.Leg.IncidentType]
        INCIDENT_UNKNOWN: TripInfo.Leg.IncidentType
        INCIDENT_NONE: TripInfo.Leg.IncidentType
        INCIDENT_CLOSURE: TripInfo.Leg.IncidentType
        INCIDENT_CRASH: TripInfo.Leg.IncidentType
        INCIDENT_CONSTRUCTION: TripInfo.Leg.IncidentType
        INCIDENT_JAM: TripInfo.Leg.IncidentType
        INCIDENT_POLICE_PRESENCE: TripInfo.Leg.IncidentType
        INCIDENT_FIXED_SPEED_CAMERA: TripInfo.Leg.IncidentType
        class EnergyConsumption(_message.Message):
            __slots__ = ("total", "thermal", "lv", "hvac", "elevation")
            TOTAL_FIELD_NUMBER: _ClassVar[int]
            THERMAL_FIELD_NUMBER: _ClassVar[int]
            LV_FIELD_NUMBER: _ClassVar[int]
            HVAC_FIELD_NUMBER: _ClassVar[int]
            ELEVATION_FIELD_NUMBER: _ClassVar[int]
            total: float
            thermal: float
            lv: float
            hvac: float
            elevation: float
            def __init__(self, total: _Optional[float] = ..., thermal: _Optional[float] = ..., lv: _Optional[float] = ..., hvac: _Optional[float] = ..., elevation: _Optional[float] = ...) -> None: ...
        class Incident(_message.Message):
            __slots__ = ("polyline_first_index", "polyline_last_index", "type")
            POLYLINE_FIRST_INDEX_FIELD_NUMBER: _ClassVar[int]
            POLYLINE_LAST_INDEX_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            polyline_first_index: int
            polyline_last_index: int
            type: TripInfo.Leg.IncidentType
            def __init__(self, polyline_first_index: _Optional[int] = ..., polyline_last_index: _Optional[int] = ..., type: _Optional[_Union[TripInfo.Leg.IncidentType, str]] = ...) -> None: ...
        class TrafficBlock(_message.Message):
            __slots__ = ("first_index", "first_index_fraction", "last_index", "last_index_fraction", "priority")
            FIRST_INDEX_FIELD_NUMBER: _ClassVar[int]
            FIRST_INDEX_FRACTION_FIELD_NUMBER: _ClassVar[int]
            LAST_INDEX_FIELD_NUMBER: _ClassVar[int]
            LAST_INDEX_FRACTION_FIELD_NUMBER: _ClassVar[int]
            PRIORITY_FIELD_NUMBER: _ClassVar[int]
            first_index: int
            first_index_fraction: float
            last_index: int
            last_index_fraction: float
            priority: int
            def __init__(self, first_index: _Optional[int] = ..., first_index_fraction: _Optional[float] = ..., last_index: _Optional[int] = ..., last_index_fraction: _Optional[float] = ..., priority: _Optional[int] = ...) -> None: ...
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        ROAD_LABEL_FIELD_NUMBER: _ClassVar[int]
        POLYLINE_FIELD_NUMBER: _ClassVar[int]
        TRAFFIC_SLOW_FIELD_NUMBER: _ClassVar[int]
        TRAFFIC_JAM_FIELD_NUMBER: _ClassVar[int]
        TRAFFIC_SEVERE_FIELD_NUMBER: _ClassVar[int]
        ENERGY_FIELD_NUMBER: _ClassVar[int]
        INCIDENTS_FIELD_NUMBER: _ClassVar[int]
        TRAFFIC_BLOCKS_FIELD_NUMBER: _ClassVar[int]
        distance: float
        duration: float
        road_label: str
        polyline: str
        traffic_slow: _containers.RepeatedScalarFieldContainer[int]
        traffic_jam: _containers.RepeatedScalarFieldContainer[int]
        traffic_severe: _containers.RepeatedScalarFieldContainer[int]
        energy: TripInfo.Leg.EnergyConsumption
        incidents: _containers.RepeatedCompositeFieldContainer[TripInfo.Leg.Incident]
        traffic_blocks: _containers.RepeatedCompositeFieldContainer[TripInfo.Leg.TrafficBlock]
        def __init__(self, distance: _Optional[float] = ..., duration: _Optional[float] = ..., road_label: _Optional[str] = ..., polyline: _Optional[str] = ..., traffic_slow: _Optional[_Iterable[int]] = ..., traffic_jam: _Optional[_Iterable[int]] = ..., traffic_severe: _Optional[_Iterable[int]] = ..., energy: _Optional[_Union[TripInfo.Leg.EnergyConsumption, _Mapping]] = ..., incidents: _Optional[_Iterable[_Union[TripInfo.Leg.Incident, _Mapping]]] = ..., traffic_blocks: _Optional[_Iterable[_Union[TripInfo.Leg.TrafficBlock, _Mapping]]] = ...) -> None: ...
    class AlternativeRoute(_message.Message):
        __slots__ = ("leg", "polyline", "route_index", "alternative_overlaps")
        LEG_FIELD_NUMBER: _ClassVar[int]
        POLYLINE_FIELD_NUMBER: _ClassVar[int]
        ROUTE_INDEX_FIELD_NUMBER: _ClassVar[int]
        ALTERNATIVE_OVERLAPS_FIELD_NUMBER: _ClassVar[int]
        leg: _containers.RepeatedCompositeFieldContainer[TripInfo.Leg]
        polyline: str
        route_index: int
        alternative_overlaps: _containers.RepeatedCompositeFieldContainer[TripInfo.AlternativeOverlap]
        def __init__(self, leg: _Optional[_Iterable[_Union[TripInfo.Leg, _Mapping]]] = ..., polyline: _Optional[str] = ..., route_index: _Optional[int] = ..., alternative_overlaps: _Optional[_Iterable[_Union[TripInfo.AlternativeOverlap, _Mapping]]] = ...) -> None: ...
    class AlternativeOverlap(_message.Message):
        __slots__ = ("alternative_index", "not_overlapping_segments")
        class Segment(_message.Message):
            __slots__ = ("start_drive_leg_index", "start_polyline_index", "end_drive_leg_index", "end_polyline_index")
            START_DRIVE_LEG_INDEX_FIELD_NUMBER: _ClassVar[int]
            START_POLYLINE_INDEX_FIELD_NUMBER: _ClassVar[int]
            END_DRIVE_LEG_INDEX_FIELD_NUMBER: _ClassVar[int]
            END_POLYLINE_INDEX_FIELD_NUMBER: _ClassVar[int]
            start_drive_leg_index: int
            start_polyline_index: int
            end_drive_leg_index: int
            end_polyline_index: int
            def __init__(self, start_drive_leg_index: _Optional[int] = ..., start_polyline_index: _Optional[int] = ..., end_drive_leg_index: _Optional[int] = ..., end_polyline_index: _Optional[int] = ...) -> None: ...
        ALTERNATIVE_INDEX_FIELD_NUMBER: _ClassVar[int]
        NOT_OVERLAPPING_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
        alternative_index: int
        not_overlapping_segments: _containers.RepeatedCompositeFieldContainer[TripInfo.AlternativeOverlap.Segment]
        def __init__(self, alternative_index: _Optional[int] = ..., not_overlapping_segments: _Optional[_Iterable[_Union[TripInfo.AlternativeOverlap.Segment, _Mapping]]] = ...) -> None: ...
    class RoutePreferences(_message.Message):
        __slots__ = ("current_arrival_soc", "default_arrival_soc", "road_avoidance", "charging_network_filters")
        CURRENT_ARRIVAL_SOC_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_ARRIVAL_SOC_FIELD_NUMBER: _ClassVar[int]
        ROAD_AVOIDANCE_FIELD_NUMBER: _ClassVar[int]
        CHARGING_NETWORK_FILTERS_FIELD_NUMBER: _ClassVar[int]
        current_arrival_soc: float
        default_arrival_soc: float
        road_avoidance: _containers.RepeatedScalarFieldContainer[str]
        charging_network_filters: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, current_arrival_soc: _Optional[float] = ..., default_arrival_soc: _Optional[float] = ..., road_avoidance: _Optional[_Iterable[str]] = ..., charging_network_filters: _Optional[_Iterable[str]] = ...) -> None: ...
    class FasterRoute(_message.Message):
        __slots__ = ("route", "time_saved")
        ROUTE_FIELD_NUMBER: _ClassVar[int]
        TIME_SAVED_FIELD_NUMBER: _ClassVar[int]
        route: TripInfo.Trip
        time_saved: float
        def __init__(self, route: _Optional[_Union[TripInfo.Trip, _Mapping]] = ..., time_saved: _Optional[float] = ...) -> None: ...
    TRIP_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    TRIP_FIELD_NUMBER: _ClassVar[int]
    ROUTE_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SOC_FIELD_NUMBER: _ClassVar[int]
    NEXT_WAYPOINT_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    FASTER_ROUTE_FIELD_NUMBER: _ClassVar[int]
    trip_id: str
    origin: GpsFix
    trip: TripInfo.Trip
    route_preferences: TripInfo.RoutePreferences
    origin_soc: float
    next_waypoint_departure: Timestamp
    faster_route: TripInfo.FasterRoute
    def __init__(self, trip_id: _Optional[str] = ..., origin: _Optional[_Union[GpsFix, _Mapping]] = ..., trip: _Optional[_Union[TripInfo.Trip, _Mapping]] = ..., route_preferences: _Optional[_Union[TripInfo.RoutePreferences, _Mapping]] = ..., origin_soc: _Optional[float] = ..., next_waypoint_departure: _Optional[_Union[Timestamp, _Mapping]] = ..., faster_route: _Optional[_Union[TripInfo.FasterRoute, _Mapping]] = ...) -> None: ...

class TripProgress(_message.Message):
    __slots__ = ("next_waypoint", "final_destination", "next_stop_index", "distance_remaining", "duration_remaining", "location_fix")
    NEXT_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
    FINAL_DESTINATION_FIELD_NUMBER: _ClassVar[int]
    NEXT_STOP_INDEX_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DURATION_REMAINING_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIX_FIELD_NUMBER: _ClassVar[int]
    next_waypoint: Timestamp
    final_destination: Timestamp
    next_stop_index: int
    distance_remaining: float
    duration_remaining: float
    location_fix: GpsFix
    def __init__(self, next_waypoint: _Optional[_Union[Timestamp, _Mapping]] = ..., final_destination: _Optional[_Union[Timestamp, _Mapping]] = ..., next_stop_index: _Optional[int] = ..., distance_remaining: _Optional[float] = ..., duration_remaining: _Optional[float] = ..., location_fix: _Optional[_Union[GpsFix, _Mapping]] = ...) -> None: ...
