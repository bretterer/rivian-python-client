"""Decoders for `navigation.*` RVM topics."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Final

from google.protobuf.message import Message

from ..utils import from_epoch
from .core import RVMDecoder, _enum, _present
from .proto import navigation_pb2


def _parse_route_switches(raw: list[str]) -> dict[str, bool]:
    """Parse `"switchName:true"` / `"switchName:false"` strings into a dict."""
    result: dict[str, bool] = {}
    for entry in raw:
        name, _, value = entry.partition(":")
        if name:
            result[name] = value.strip().lower() == "true"
    return result


TripInfo = navigation_pb2.TripInfo

_STOP_STATUS_MAP: Final[dict[int, str]] = {
    navigation_pb2.STOP_STATUS_STOPPING: "stopping",
    navigation_pb2.STOP_STATUS_ARRIVED: "arrived",
    navigation_pb2.STOP_STATUS_NEXT_STOP: "next_stop",
    navigation_pb2.STOP_STATUS_FUTURE: "future",
}

_CHARGE_DATA_ACCURACY_MAP: Final[dict[int, str]] = {
    TripInfo.CHARGE_DATA_ACCURACY_OK: "ok",
    TripInfo.CHARGE_DATA_ACCURACY_CONSUMPTION_FAILED: "consumption_failed",
    TripInfo.CHARGE_DATA_ACCURACY_CHARGETIME_FAILED: "chargetime_failed",
    TripInfo.CHARGE_DATA_ACCURACY_BOTH_FAILED: "both_failed",
}

_INCIDENT_MAP: Final[dict[int, str]] = {
    TripInfo.Leg.INCIDENT_UNKNOWN: "unknown",
    TripInfo.Leg.INCIDENT_NONE: "none",
    TripInfo.Leg.INCIDENT_CLOSURE: "closure",
    TripInfo.Leg.INCIDENT_CRASH: "crash",
    TripInfo.Leg.INCIDENT_CONSTRUCTION: "construction",
    TripInfo.Leg.INCIDENT_JAM: "jam",
    TripInfo.Leg.INCIDENT_POLICE_PRESENCE: "police_presence",
    TripInfo.Leg.INCIDENT_FIXED_SPEED_CAMERA: "fixed_speed_camera",
}


def _copy_present(
    message: Message, pairs: tuple[tuple[str, str], ...]
) -> dict[str, Any]:
    """`{key: value}` for each `(field, key)` in `pairs` that was sent."""
    return {
        key: value
        for field, key in pairs
        if (value := _present(message, field)) is not None
    }


def _decode_geocoordinate(
    loc: navigation_pb2.GeoCoordinate | None, latitude_key: str, longitude_key: str
) -> dict[str, Any]:
    """Decode a GeoCoordinate into the given keys."""
    if loc is None:
        return {}
    return _copy_present(
        loc, (("latitude", latitude_key), ("longitude", longitude_key))
    )


def _decode_timestamp(wrapper: Message | None) -> datetime | None:
    """Decode a {seconds, nanos} time wrapper (nanos optional)."""
    if wrapper is None or (seconds := _present(wrapper, "seconds")) is None:
        return None
    nanos = getattr(wrapper, "nanos", 0)
    return from_epoch(seconds + nanos / 1e9)


def _decode_origin(origin: navigation_pb2.GpsFix) -> dict[str, Any]:
    """Decode trip_info's origin submessage."""
    result = _decode_geocoordinate(
        _present(origin, "location"), "originLatitude", "originLongitude"
    )
    result["originHeading"] = origin.heading
    if (origin_epoch := _present(origin, "time")) is not None:
        result["originTime"] = from_epoch(origin_epoch)
    return result


def _decode_place(place: TripInfo.Place) -> dict[str, Any]:
    """Decode a `type: "place"` waypoint."""
    entry: dict[str, Any] = {"type": "place"}
    entry.update(
        _decode_geocoordinate(_present(place, "location"), "latitude", "longitude")
    )
    # Only surface the road-snapped location when it differs.
    snapped = _decode_geocoordinate(
        _present(place, "snapped_location"), "snappedLatitude", "snappedLongitude"
    )
    if any(
        abs(snapped[snapped_key] - entry.get(key, snapped[snapped_key])) > 1e-5
        for key, snapped_key in (
            ("latitude", "snappedLatitude"),
            ("longitude", "snappedLongitude"),
        )
        if snapped_key in snapped
    ):
        entry.update(snapped)
    entry["status"] = _enum(_STOP_STATUS_MAP, place.status, what="stop status")
    entry.update(_copy_present(place, (("name", "name"), ("place_id", "placeId"))))
    entry["stopDuration"] = place.stop_duration
    entry["stateOfCharge"] = place.soc
    entry["rangeRemaining"] = place.range
    if (arrival := _decode_timestamp(_present(place, "arrival"))) is not None:
        entry["arrivalTime"] = arrival
    return entry


def _decode_charging_stop(charge: TripInfo.ChargingStop) -> dict[str, Any]:
    """Decode a `type: "chargingStop"` waypoint."""
    entry: dict[str, Any] = {"type": "chargingStop"}
    entry.update(
        _copy_present(charge, (("station_id", "stationId"), ("label", "label")))
    )
    entry.update(
        _decode_geocoordinate(_present(charge, "location"), "latitude", "longitude")
    )
    entry.update(
        _copy_present(
            charge,
            (
                ("charge_duration", "chargeDuration"),
                ("arrival_soc", "arrivalStateOfCharge"),
                ("arrival_range", "arrivalRangeRemaining"),
                ("departure_soc", "departureStateOfCharge"),
                ("departure_range", "departureRangeRemaining"),
            ),
        )
    )
    departure = _decode_timestamp(_present(charge, "departure_time"))
    if departure is not None:
        entry["departureTime"] = departure
    arrival = _decode_timestamp(_present(charge, "arrival_time"))
    if arrival is not None:
        entry["arrivalTime"] = arrival
    entry["chargeDataAccuracy"] = _enum(
        _CHARGE_DATA_ACCURACY_MAP, charge.charge_data_accuracy, what="charge data"
    )
    entry["isSystemAdded"] = charge.is_system_added
    entry["compatible"] = charge.compatible
    entry["adapterRequired"] = charge.adapter_required
    entry["stopDuration"] = charge.stop_duration
    entry["status"] = _enum(_STOP_STATUS_MAP, charge.status, what="stop status")
    return entry


def _decode_waypoints(trip: TripInfo.Trip) -> list[dict[str, Any]]:
    """Decode every waypoint, in order."""
    waypoints: list[dict[str, Any]] = []
    for wrapper in trip.waypoint:
        if wrapper.HasField("place"):
            waypoints.append(_decode_place(wrapper.place))
        elif wrapper.HasField("charging_stop"):
            waypoints.append(_decode_charging_stop(wrapper.charging_stop))
    return waypoints


def _decode_traffic_blocks(leg: TripInfo.Leg) -> list[dict[str, Any]]:
    """Decode a leg's traffic blocks."""
    return [
        {
            "firstIndex": block.first_index,
            "firstIndexFraction": round(block.first_index_fraction, 4),
            "lastIndex": block.last_index,
            "lastIndexFraction": round(block.last_index_fraction, 4),
            "priority": block.priority,
        }
        for block in leg.traffic_blocks
    ]


def _decode_incidents(leg: TripInfo.Leg) -> list[dict[str, Any]]:
    """Decode a leg's traffic incidents."""
    return [
        {
            "firstIndex": incident.polyline_first_index,
            "lastIndex": incident.polyline_last_index,
            "type": _enum(_INCIDENT_MAP, incident.type, what="traffic incident"),
        }
        for incident in leg.incidents
    ]


def _decode_leg(leg: TripInfo.Leg) -> dict[str, Any]:
    """Decode one route leg."""
    entry: dict[str, Any] = {"distance": leg.distance, "duration": leg.duration}
    entry.update(
        _copy_present(leg, (("road_label", "roadLabel"), ("polyline", "polyline")))
    )
    if leg.HasField("energy"):
        energy = leg.energy
        entry["energyConsumption"] = {
            "total": energy.total,
            "thermal": energy.thermal,
            "lv": energy.lv,
            "hvac": energy.hvac,
            "elevation": energy.elevation,
        }
    # traffic_slow/jam/severe repeat the traffic blocks as index pairs.
    if traffic_blocks := _decode_traffic_blocks(leg):
        entry["trafficBlocks"] = traffic_blocks
    if incidents := _decode_incidents(leg):
        entry["incidents"] = incidents
    return entry


def _decode_trip(trip: TripInfo.Trip) -> dict[str, Any]:
    """Decode trip_info's trip submessage: totals, waypoints, legs."""
    result = _copy_present(
        trip,
        (
            ("distance", "distance"),
            ("duration", "duration"),
        ),
    )
    if waypoints := _decode_waypoints(trip):
        result["waypoints"] = waypoints
    if legs := [_decode_leg(leg) for leg in trip.leg]:
        result["legs"] = legs
    result.update(
        _copy_present(
            trip,
            (
                ("overview_polyline", "overviewPolyline"),
                ("final_soc", "finalStateOfCharge"),
                ("final_range", "finalRangeRemaining"),
            ),
        )
    )
    result["socIsBelowLimit"] = trip.soc_is_below_limit
    if trip.HasField("battery_empty_location"):
        result.update(
            _decode_geocoordinate(
                trip.battery_empty_location,
                "batteryEmptyLatitude",
                "batteryEmptyLongitude",
            )
        )
        result["batteryEmptyToDestinationDistance"] = (
            trip.battery_empty_to_destination_distance
        )
    return result


def _decode_route_preferences(prefs: TripInfo.RoutePreferences) -> dict[str, Any]:
    """Decode trip_info's route preferences."""
    result = _copy_present(
        prefs,
        (
            ("current_arrival_soc", "currentArrivalSoc"),
            ("default_arrival_soc", "defaultArrivalSoc"),
        ),
    )
    for field, key in (
        ("road_avoidance", "roadAvoidance"),
        ("charging_network_filters", "chargingNetworkFilters"),
    ):
        if switches := _parse_route_switches(list(getattr(prefs, field))):
            result[key] = switches
    return result


@RVMDecoder.register("navigation.navigation_service.trip_info", navigation_pb2.TripInfo)
def decode_trip_info(m: navigation_pb2.TripInfo) -> dict[str, Any]:
    """navigation.navigation_service.trip_info — the planned trip.

    Fields:
        tripId: str — changes on every route computation, so it can't
            correlate messages
        originLatitude, originLongitude: float
        originHeading: float (degrees)
        originTime: datetime
        originStateOfCharge: float (percent)
        distance, duration: float — driving totals (meters, seconds),
            excluding charging stops
        waypoints: list[dict] — stops in order; `legs[i]` is the route to
            `waypoints[i]`. Each has `type` ("place" | "chargingStop"),
            latitude, longitude and arrivalTime. A charger the user chose
            is a place.
            Both types also have status ("stopping" | "arrived" |
                "next_stop" | "future") and stopDuration (seconds).
            place: name, placeId (Google Place ID or Rivian charger ID),
                stateOfCharge and rangeRemaining on arrival (percent,
                meters), and snappedLatitude/snappedLongitude when the
                road-snapped location differs
            chargingStop: stationId, label (address with the network in
                brackets), chargeDuration (seconds), arrival/departure
                StateOfCharge and RangeRemaining (percent, meters),
                departureTime, chargeDataAccuracy, isSystemAdded,
                compatible, adapterRequired
        legs: list[dict] — distance, duration (meters, seconds),
            roadLabel, polyline (Google-encoded), energyConsumption
            ({total, thermal, lv, hvac, elevation}, kWh), trafficBlocks
            ({firstIndex, firstIndexFraction, lastIndex, lastIndexFraction,
            priority}; polyline index ranges, fractions 0-1 past a point)
            and incidents ({firstIndex, lastIndex, type})
        overviewPolyline: str — Google-encoded, whole trip
        nextWaypointDepartureTime: datetime — the next stop's departure if
            it's a charging stop, else its arrival
        finalStateOfCharge, finalRangeRemaining: float — the last
            waypoint's (percent, meters)
        socIsBelowLimit: bool
        batteryEmptyLatitude, batteryEmptyLongitude: float, and
            batteryEmptyToDestinationDistance: float (meters) — when the
            route runs out of charge
        currentArrivalSoc, defaultArrivalSoc: float (fraction, 0-1)
        fasterRouteTimeSaved: float (seconds), when a faster route exists
        roadAvoidance, chargingNetworkFilters: dict[str, bool] — app
            toggles, e.g. "switchExcludeMotorway", "switchRivianFilter"
    """
    result = _copy_present(m, (("trip_id", "tripId"),))
    if m.HasField("origin"):
        result.update(_decode_origin(m.origin))
    if m.HasField("trip"):
        result.update(_decode_trip(m.trip))
    next_departure = _decode_timestamp(_present(m, "next_waypoint_departure"))
    if next_departure is not None:
        result["nextWaypointDepartureTime"] = next_departure
    if (v := _present(m, "origin_soc")) is not None:
        result["originStateOfCharge"] = v
    if m.HasField("route_preferences"):
        result.update(_decode_route_preferences(m.route_preferences))
    if m.HasField("faster_route"):
        result["fasterRouteTimeSaved"] = m.faster_route.time_saved
    return result


@RVMDecoder.register(
    "navigation.navigation_service.trip_progress", navigation_pb2.TripProgress
)
def decode_trip_progress(m: navigation_pb2.TripProgress) -> dict[str, Any]:
    """navigation.navigation_service.trip_progress — live progress on the active trip.

    Fields:
        nextWaypointArrivalTime: datetime — live ETA
        finalDestinationArrivalTime: datetime — live ETA for the last
            waypoint; missing for one message after the waypoints change
        nextStopIndex: int
        distanceRemaining, durationRemaining: float — to the next waypoint
            (meters, seconds)
        latitude, longitude: float
        speed: float (m/s)
        heading: float (degrees)
        locationTime: datetime — time of the position fix
    """
    result: dict[str, Any] = {}
    if (eta := _decode_timestamp(_present(m, "next_waypoint"))) is not None:
        result["nextWaypointArrivalTime"] = eta
    if (eta := _decode_timestamp(_present(m, "final_destination"))) is not None:
        result["finalDestinationArrivalTime"] = eta
    result["nextStopIndex"] = m.next_stop_index
    result["distanceRemaining"] = m.distance_remaining
    result["durationRemaining"] = m.duration_remaining
    if m.HasField("location_fix"):
        fix = m.location_fix
        result.update(
            _decode_geocoordinate(_present(fix, "location"), "latitude", "longitude")
        )
        result["speed"] = fix.speed
        result["heading"] = fix.heading
        if (fix_epoch := _present(fix, "time")) is not None:
            result["locationTime"] = from_epoch(fix_epoch)
    return result
