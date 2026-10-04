"""Decoders for `navigation.*` RVM topics."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from google.protobuf.message import Message

from ..utils import from_epoch
from .core import RVMDecoder, _present
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


def _decode_origin(origin: TripInfo.Origin) -> dict[str, Any]:
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
    entry.update(
        _copy_present(
            place,
            (
                ("place_type", "placeType"),
                ("name", "name"),
                ("place_id", "placeId"),
            ),
        )
    )
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


def _decode_index_ranges(leg: TripInfo.Leg) -> list[dict[str, Any]]:
    """Decode a leg's `indexRangeSegments`."""
    return [
        {
            **_copy_present(seg, (("start", "start"), ("end", "end"))),
            "startFraction": round(seg.start_fraction, 4),
            "endFraction": round(seg.end_fraction, 4),
            "flagged": seg.HasField("flag"),
        }
        for seg in leg.index_range_segment
    ]


def _decode_categorized_ranges(leg: TripInfo.Leg) -> list[dict[str, Any]]:
    """Decode a leg's `categorizedIndexRanges`."""
    ranges = (
        _copy_present(
            seg, (("start", "start"), ("end", "end"), ("category", "category"))
        )
        for seg in leg.categorized_range_segment
    )
    return [entry for entry in ranges if entry]


def _decode_leg(leg: TripInfo.Leg) -> dict[str, Any]:
    """Decode one route leg."""
    entry: dict[str, Any] = {"distance": leg.distance, "duration": leg.duration}
    entry.update(
        _copy_present(leg, (("road_label", "roadLabel"), ("polyline", "polyline")))
    )
    if leg.HasField("energy"):
        entry["energyUsed"] = leg.energy.kwh
    # flagged/unflagged_ranges_packed duplicate the index ranges.
    if index_ranges := _decode_index_ranges(leg):
        entry["indexRangeSegments"] = index_ranges
    if categorized_ranges := _decode_categorized_ranges(leg):
        entry["categorizedIndexRanges"] = categorized_ranges
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
    return result


def _decode_route_preferences(prefs: TripInfo.RoutePreferences) -> dict[str, Any]:
    """Decode trip_info's route preferences."""
    result = _copy_present(
        prefs, (("weight_a", "routeWeightA"), ("weight_b", "routeWeightB"))
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
            place: placeType (2 for the next stop, 3 after), name,
                placeId (Google Place ID or Rivian charger ID),
                stateOfCharge and rangeRemaining on arrival (percent,
                meters), and snappedLatitude/snappedLongitude when the
                road-snapped location differs
            chargingStop: stationId, label (address with the network in
                brackets), chargeDuration (seconds; the stop runs a few
                minutes longer), arrival/departure StateOfCharge and
                RangeRemaining (percent, meters), departureTime
        legs: list[dict] — distance, duration (meters, seconds),
            roadLabel, polyline (Google-encoded), energyUsed (kWh;
            unverified), indexRangeSegments ({start, startFraction, end,
            endFraction, flagged}; fractions are 0-1 positions past those
            points) and categorizedIndexRanges ({start, end, category}),
            index ranges into the polyline whose meaning is unknown
        overviewPolyline: str — Google-encoded, whole trip
        nextWaypointDepartureTime: datetime — the next stop's departure if
            it's a charging stop, else its arrival
        finalStateOfCharge, finalRangeRemaining: float — the last
            waypoint's (percent, meters)
        routeWeightA, routeWeightB: float — unknown
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
