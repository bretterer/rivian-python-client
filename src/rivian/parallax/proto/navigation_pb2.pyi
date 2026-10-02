from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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

class TripInfo(_message.Message):
    __slots__ = ("trip_id", "origin", "trip", "route_preferences", "origin_soc", "next_waypoint_departure")
    class Origin(_message.Message):
        __slots__ = ("location", "heading", "time")
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        HEADING_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        location: GeoCoordinate
        heading: float
        time: int
        def __init__(self, location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., heading: _Optional[float] = ..., time: _Optional[int] = ...) -> None: ...
    class NextWaypointDeparture(_message.Message):
        __slots__ = ("seconds",)
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        def __init__(self, seconds: _Optional[int] = ...) -> None: ...
    class Trip(_message.Message):
        __slots__ = ("distance", "duration", "waypoint", "leg", "final_soc", "final_range", "overview_polyline", "trip_meta")
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        WAYPOINT_FIELD_NUMBER: _ClassVar[int]
        LEG_FIELD_NUMBER: _ClassVar[int]
        FINAL_SOC_FIELD_NUMBER: _ClassVar[int]
        FINAL_RANGE_FIELD_NUMBER: _ClassVar[int]
        OVERVIEW_POLYLINE_FIELD_NUMBER: _ClassVar[int]
        TRIP_META_FIELD_NUMBER: _ClassVar[int]
        distance: float
        duration: float
        waypoint: _containers.RepeatedCompositeFieldContainer[TripInfo.WaypointWrapper]
        leg: _containers.RepeatedCompositeFieldContainer[TripInfo.Leg]
        final_soc: float
        final_range: float
        overview_polyline: str
        trip_meta: TripInfo.TripMeta
        def __init__(self, distance: _Optional[float] = ..., duration: _Optional[float] = ..., waypoint: _Optional[_Iterable[_Union[TripInfo.WaypointWrapper, _Mapping]]] = ..., leg: _Optional[_Iterable[_Union[TripInfo.Leg, _Mapping]]] = ..., final_soc: _Optional[float] = ..., final_range: _Optional[float] = ..., overview_polyline: _Optional[str] = ..., trip_meta: _Optional[_Union[TripInfo.TripMeta, _Mapping]] = ...) -> None: ...
    class WaypointWrapper(_message.Message):
        __slots__ = ("place", "charging_stop")
        PLACE_FIELD_NUMBER: _ClassVar[int]
        CHARGING_STOP_FIELD_NUMBER: _ClassVar[int]
        place: TripInfo.Place
        charging_stop: TripInfo.ChargingStop
        def __init__(self, place: _Optional[_Union[TripInfo.Place, _Mapping]] = ..., charging_stop: _Optional[_Union[TripInfo.ChargingStop, _Mapping]] = ...) -> None: ...
    class Place(_message.Message):
        __slots__ = ("location", "snapped_location", "place_type", "name", "place_id", "soc", "range", "arrival")
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        SNAPPED_LOCATION_FIELD_NUMBER: _ClassVar[int]
        PLACE_TYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        PLACE_ID_FIELD_NUMBER: _ClassVar[int]
        SOC_FIELD_NUMBER: _ClassVar[int]
        RANGE_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_FIELD_NUMBER: _ClassVar[int]
        location: GeoCoordinate
        snapped_location: GeoCoordinate
        place_type: int
        name: str
        place_id: str
        soc: float
        range: float
        arrival: Timestamp
        def __init__(self, location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., snapped_location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., place_type: _Optional[int] = ..., name: _Optional[str] = ..., place_id: _Optional[str] = ..., soc: _Optional[float] = ..., range: _Optional[float] = ..., arrival: _Optional[_Union[Timestamp, _Mapping]] = ...) -> None: ...
    class ChargingStop(_message.Message):
        __slots__ = ("station_id", "label", "location", "charge_duration", "arrival_soc", "arrival_range", "departure_soc", "departure_range", "departure_time", "arrival_time", "field_12", "field_13", "field_14", "field_17")
        class DepartureTimeWrapper(_message.Message):
            __slots__ = ("seconds",)
            SECONDS_FIELD_NUMBER: _ClassVar[int]
            seconds: int
            def __init__(self, seconds: _Optional[int] = ...) -> None: ...
        class ArrivalTimeWrapper(_message.Message):
            __slots__ = ("seconds",)
            SECONDS_FIELD_NUMBER: _ClassVar[int]
            seconds: int
            def __init__(self, seconds: _Optional[int] = ...) -> None: ...
        STATION_ID_FIELD_NUMBER: _ClassVar[int]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        CHARGE_DURATION_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_SOC_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_RANGE_FIELD_NUMBER: _ClassVar[int]
        DEPARTURE_SOC_FIELD_NUMBER: _ClassVar[int]
        DEPARTURE_RANGE_FIELD_NUMBER: _ClassVar[int]
        DEPARTURE_TIME_FIELD_NUMBER: _ClassVar[int]
        ARRIVAL_TIME_FIELD_NUMBER: _ClassVar[int]
        FIELD_12_FIELD_NUMBER: _ClassVar[int]
        FIELD_13_FIELD_NUMBER: _ClassVar[int]
        FIELD_14_FIELD_NUMBER: _ClassVar[int]
        FIELD_17_FIELD_NUMBER: _ClassVar[int]
        station_id: str
        label: str
        location: GeoCoordinate
        charge_duration: float
        arrival_soc: float
        arrival_range: float
        departure_soc: float
        departure_range: float
        departure_time: TripInfo.ChargingStop.DepartureTimeWrapper
        arrival_time: TripInfo.ChargingStop.ArrivalTimeWrapper
        field_12: int
        field_13: int
        field_14: int
        field_17: int
        def __init__(self, station_id: _Optional[str] = ..., label: _Optional[str] = ..., location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., charge_duration: _Optional[float] = ..., arrival_soc: _Optional[float] = ..., arrival_range: _Optional[float] = ..., departure_soc: _Optional[float] = ..., departure_range: _Optional[float] = ..., departure_time: _Optional[_Union[TripInfo.ChargingStop.DepartureTimeWrapper, _Mapping]] = ..., arrival_time: _Optional[_Union[TripInfo.ChargingStop.ArrivalTimeWrapper, _Mapping]] = ..., field_12: _Optional[int] = ..., field_13: _Optional[int] = ..., field_14: _Optional[int] = ..., field_17: _Optional[int] = ...) -> None: ...
    class Leg(_message.Message):
        __slots__ = ("distance", "duration", "road_label", "polyline", "flagged_ranges_packed", "unflagged_ranges_packed", "energy", "categorized_range_segment", "index_range_segment")
        class Energy(_message.Message):
            __slots__ = ("kwh",)
            KWH_FIELD_NUMBER: _ClassVar[int]
            kwh: float
            def __init__(self, kwh: _Optional[float] = ...) -> None: ...
        class CategorizedRangeSegment(_message.Message):
            __slots__ = ("start", "end", "category")
            START_FIELD_NUMBER: _ClassVar[int]
            END_FIELD_NUMBER: _ClassVar[int]
            CATEGORY_FIELD_NUMBER: _ClassVar[int]
            start: int
            end: int
            category: int
            def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ..., category: _Optional[int] = ...) -> None: ...
        class IndexRangeSegment(_message.Message):
            __slots__ = ("start", "start_fraction", "end", "end_fraction", "flag")
            START_FIELD_NUMBER: _ClassVar[int]
            START_FRACTION_FIELD_NUMBER: _ClassVar[int]
            END_FIELD_NUMBER: _ClassVar[int]
            END_FRACTION_FIELD_NUMBER: _ClassVar[int]
            FLAG_FIELD_NUMBER: _ClassVar[int]
            start: int
            start_fraction: float
            end: int
            end_fraction: float
            flag: bool
            def __init__(self, start: _Optional[int] = ..., start_fraction: _Optional[float] = ..., end: _Optional[int] = ..., end_fraction: _Optional[float] = ..., flag: _Optional[bool] = ...) -> None: ...
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        ROAD_LABEL_FIELD_NUMBER: _ClassVar[int]
        POLYLINE_FIELD_NUMBER: _ClassVar[int]
        FLAGGED_RANGES_PACKED_FIELD_NUMBER: _ClassVar[int]
        UNFLAGGED_RANGES_PACKED_FIELD_NUMBER: _ClassVar[int]
        ENERGY_FIELD_NUMBER: _ClassVar[int]
        CATEGORIZED_RANGE_SEGMENT_FIELD_NUMBER: _ClassVar[int]
        INDEX_RANGE_SEGMENT_FIELD_NUMBER: _ClassVar[int]
        distance: float
        duration: float
        road_label: str
        polyline: str
        flagged_ranges_packed: bytes
        unflagged_ranges_packed: bytes
        energy: TripInfo.Leg.Energy
        categorized_range_segment: _containers.RepeatedCompositeFieldContainer[TripInfo.Leg.CategorizedRangeSegment]
        index_range_segment: _containers.RepeatedCompositeFieldContainer[TripInfo.Leg.IndexRangeSegment]
        def __init__(self, distance: _Optional[float] = ..., duration: _Optional[float] = ..., road_label: _Optional[str] = ..., polyline: _Optional[str] = ..., flagged_ranges_packed: _Optional[bytes] = ..., unflagged_ranges_packed: _Optional[bytes] = ..., energy: _Optional[_Union[TripInfo.Leg.Energy, _Mapping]] = ..., categorized_range_segment: _Optional[_Iterable[_Union[TripInfo.Leg.CategorizedRangeSegment, _Mapping]]] = ..., index_range_segment: _Optional[_Iterable[_Union[TripInfo.Leg.IndexRangeSegment, _Mapping]]] = ...) -> None: ...
    class RoutePreferences(_message.Message):
        __slots__ = ("weight_a", "weight_b", "road_avoidance", "charging_network_filters")
        WEIGHT_A_FIELD_NUMBER: _ClassVar[int]
        WEIGHT_B_FIELD_NUMBER: _ClassVar[int]
        ROAD_AVOIDANCE_FIELD_NUMBER: _ClassVar[int]
        CHARGING_NETWORK_FILTERS_FIELD_NUMBER: _ClassVar[int]
        weight_a: float
        weight_b: float
        road_avoidance: _containers.RepeatedScalarFieldContainer[str]
        charging_network_filters: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, weight_a: _Optional[float] = ..., weight_b: _Optional[float] = ..., road_avoidance: _Optional[_Iterable[str]] = ..., charging_network_filters: _Optional[_Iterable[str]] = ...) -> None: ...
    class TripMeta(_message.Message):
        __slots__ = ("field_1", "field_2", "field_3", "field_4")
        class Unmapped2(_message.Message):
            __slots__ = ("field_2", "field_4")
            FIELD_2_FIELD_NUMBER: _ClassVar[int]
            FIELD_4_FIELD_NUMBER: _ClassVar[int]
            field_2: int
            field_4: int
            def __init__(self, field_2: _Optional[int] = ..., field_4: _Optional[int] = ...) -> None: ...
        FIELD_1_FIELD_NUMBER: _ClassVar[int]
        FIELD_2_FIELD_NUMBER: _ClassVar[int]
        FIELD_3_FIELD_NUMBER: _ClassVar[int]
        FIELD_4_FIELD_NUMBER: _ClassVar[int]
        field_1: int
        field_2: TripInfo.TripMeta.Unmapped2
        field_3: int
        field_4: int
        def __init__(self, field_1: _Optional[int] = ..., field_2: _Optional[_Union[TripInfo.TripMeta.Unmapped2, _Mapping]] = ..., field_3: _Optional[int] = ..., field_4: _Optional[int] = ...) -> None: ...
    TRIP_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    TRIP_FIELD_NUMBER: _ClassVar[int]
    ROUTE_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SOC_FIELD_NUMBER: _ClassVar[int]
    NEXT_WAYPOINT_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    trip_id: str
    origin: TripInfo.Origin
    trip: TripInfo.Trip
    route_preferences: TripInfo.RoutePreferences
    origin_soc: float
    next_waypoint_departure: TripInfo.NextWaypointDeparture
    def __init__(self, trip_id: _Optional[str] = ..., origin: _Optional[_Union[TripInfo.Origin, _Mapping]] = ..., trip: _Optional[_Union[TripInfo.Trip, _Mapping]] = ..., route_preferences: _Optional[_Union[TripInfo.RoutePreferences, _Mapping]] = ..., origin_soc: _Optional[float] = ..., next_waypoint_departure: _Optional[_Union[TripInfo.NextWaypointDeparture, _Mapping]] = ...) -> None: ...

class TripProgress(_message.Message):
    __slots__ = ("next_waypoint", "final_destination", "distance_remaining", "duration_remaining", "location_fix")
    class NextWaypoint(_message.Message):
        __slots__ = ("seconds",)
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        def __init__(self, seconds: _Optional[int] = ...) -> None: ...
    class FinalDestination(_message.Message):
        __slots__ = ("seconds",)
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        def __init__(self, seconds: _Optional[int] = ...) -> None: ...
    class LocationFix(_message.Message):
        __slots__ = ("location", "speed", "heading", "time")
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        SPEED_FIELD_NUMBER: _ClassVar[int]
        HEADING_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        location: GeoCoordinate
        speed: float
        heading: float
        time: int
        def __init__(self, location: _Optional[_Union[GeoCoordinate, _Mapping]] = ..., speed: _Optional[float] = ..., heading: _Optional[float] = ..., time: _Optional[int] = ...) -> None: ...
    NEXT_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
    FINAL_DESTINATION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DURATION_REMAINING_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIX_FIELD_NUMBER: _ClassVar[int]
    next_waypoint: TripProgress.NextWaypoint
    final_destination: TripProgress.FinalDestination
    distance_remaining: float
    duration_remaining: float
    location_fix: TripProgress.LocationFix
    def __init__(self, next_waypoint: _Optional[_Union[TripProgress.NextWaypoint, _Mapping]] = ..., final_destination: _Optional[_Union[TripProgress.FinalDestination, _Mapping]] = ..., distance_remaining: _Optional[float] = ..., duration_remaining: _Optional[float] = ..., location_fix: _Optional[_Union[TripProgress.LocationFix, _Mapping]] = ...) -> None: ...
