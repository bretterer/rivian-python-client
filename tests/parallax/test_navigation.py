"""Tests for the `navigation.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import navigation_pb2 as nav

from .helpers import decode, epoch


def test_trip_info() -> None:
    """Origin, waypoints of both types, legs, and route preferences."""
    trip = nav.TripInfo
    stop = trip.ChargingStop
    result = decode(
        "navigation.navigation_service.trip_info",
        trip(
            trip_id="-123",
            origin=trip.Origin(
                location=nav.GeoCoordinate(latitude=33.1, longitude=-80.2),
                time=1790553420000,
            ),
            trip=trip.Trip(
                distance=1000.0,
                duration=600.0,
                waypoint=[
                    trip.WaypointWrapper(
                        place=trip.Place(
                            location=nav.GeoCoordinate(latitude=33.1, longitude=-80.1),
                            snapped_location=nav.GeoCoordinate(
                                latitude=33.1, longitude=-80.1
                            ),
                            place_type=2,
                            name="Store",
                            arrival=nav.Timestamp(seconds=1790554000),
                        )
                    ),
                    trip.WaypointWrapper(
                        charging_stop=stop(
                            station_id="100103",
                            location=nav.GeoCoordinate(latitude=34.0, longitude=-81.0),
                            charge_duration=1800.0,
                            departure_time=stop.DepartureTimeWrapper(
                                seconds=1790558000
                            ),
                            arrival_time=stop.ArrivalTimeWrapper(seconds=1790556200),
                        )
                    ),
                ],
                leg=[
                    trip.Leg(
                        distance=500.0,
                        polyline="poly",
                        index_range_segment=[
                            trip.Leg.IndexRangeSegment(start=1, end=4)
                        ],
                    )
                ],
                overview_polyline="overview",
            ),
            route_preferences=trip.RoutePreferences(
                weight_a=0.25,
                road_avoidance=["switchExcludeToll:true"],
                charging_network_filters=[
                    "switchRivianFilter:true",
                    "switchChargePointFilter:false",
                ],
            ),
            next_waypoint_departure=trip.NextWaypointDeparture(seconds=1790558000),
        ),
    )
    assert result["tripId"] == "-123"
    assert result["originLatitude"] == 33.1
    assert result["originTime"] == epoch(1790553420000)
    assert result["distance"] == 1000.0
    place, charger = result["waypoints"]
    assert place == {  # an identical snapped location is not surfaced
        "type": "place",
        "latitude": 33.1,
        "longitude": -80.1,
        "placeType": 2,
        "name": "Store",
        "arrivalTime": epoch(1790554000_000),
    }
    assert charger["type"] == "chargingStop"
    assert charger["stationId"] == "100103"
    assert charger["chargeDuration"] == 1800.0
    assert charger["arrivalTime"] == epoch(1790556200_000)
    assert charger["departureTime"] == epoch(1790558000_000)
    assert result["legs"] == [
        {
            "distance": 500.0,
            "polyline": "poly",
            "indexRangeSegments": [{"start": 1, "end": 4, "flagged": False}],
        }
    ]
    assert result["overviewPolyline"] == "overview"
    assert result["routeWeightA"] == 0.25
    assert result["roadAvoidance"] == {"switchExcludeToll": True}
    assert result["chargingNetworkFilters"] == {
        "switchRivianFilter": True,
        "switchChargePointFilter": False,
    }
    assert result["nextWaypointDepartureTime"] == epoch(1790558000_000)


def test_trip_info_snapped_location() -> None:
    """A snapped location that differs from the pin is surfaced."""
    trip = nav.TripInfo
    place = trip.Place(
        location=nav.GeoCoordinate(latitude=33.1, longitude=-80.1),
        snapped_location=nav.GeoCoordinate(latitude=33.1, longitude=-80.10002),
    )
    result = decode(
        "navigation.navigation_service.trip_info",
        trip(trip=trip.Trip(waypoint=[trip.WaypointWrapper(place=place)])),
    )
    assert result["waypoints"][0]["snappedLongitude"] == -80.10002


def test_trip_progress() -> None:
    """ETAs, remaining distance, and the live location fix."""
    progress = nav.TripProgress
    result = decode(
        "navigation.navigation_service.trip_progress",
        progress(
            next_waypoint=progress.NextWaypoint(seconds=1790553420),
            distance_remaining=54.0,
            location_fix=progress.LocationFix(
                location=nav.GeoCoordinate(latitude=33.4, longitude=-80.8),
                speed=10.5,
                time=1790553428211,
            ),
        ),
    )
    assert result == {
        "nextWaypointArrivalTime": epoch(1790553420_000),
        "distanceRemaining": 54.0,
        "latitude": 33.4,
        "longitude": -80.8,
        "speed": 10.5,
        "locationTime": epoch(1790553428211),
    }
