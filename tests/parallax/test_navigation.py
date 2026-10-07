"""Tests for the `navigation.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import navigation_pb2 as nav

from .helpers import decode, epoch


def test_trip_info() -> None:
    """Origin, waypoints of both types, legs, and route preferences."""
    trip = nav.TripInfo
    stop = trip.ChargingStop
    leg = trip.Leg
    result = decode(
        "navigation.navigation_service.trip_info",
        trip(
            trip_id="-123",
            origin=nav.GpsFix(
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
                            status=nav.STOP_STATUS_NEXT_STOP,
                            name="Store",
                            arrival=nav.Timestamp(seconds=1790554000),
                        )
                    ),
                    trip.WaypointWrapper(
                        charging_stop=stop(
                            station_id="100103",
                            location=nav.GeoCoordinate(latitude=34.0, longitude=-81.0),
                            charge_duration=1800.0,
                            departure_time=nav.Timestamp(seconds=1790558000),
                            arrival_time=nav.Timestamp(seconds=1790556200),
                            compatible=True,
                            status=nav.STOP_STATUS_FUTURE,
                        )
                    ),
                ],
                leg=[
                    leg(
                        distance=500.0,
                        polyline="poly",
                        energy=leg.EnergyConsumption(total=2500.0, hvac=300.0),
                        incidents=[
                            leg.Incident(
                                polyline_first_index=3,
                                polyline_last_index=9,
                                type=leg.INCIDENT_CONSTRUCTION,
                            )
                        ],
                        traffic_blocks=[
                            leg.TrafficBlock(
                                first_index=1,
                                first_index_fraction=0.5,
                                last_index=4,
                                last_index_fraction=0.25,
                                priority=1,
                            )
                        ],
                    )
                ],
                overview_polyline="overview",
            ),
            route_preferences=trip.RoutePreferences(
                current_arrival_soc=15.0,
                road_avoidance=["switchExcludeToll:true"],
                charging_network_filters=[
                    "switchRivianFilter:true",
                    "switchChargePointFilter:false",
                ],
            ),
            next_waypoint_departure=nav.Timestamp(seconds=1790558000),
        ),
    )
    assert result["tripId"] == "-123"
    assert result["originLatitude"] == 33.1
    assert result["originTime"] == epoch(1790553420000)
    assert result["distance"] == 1000.0
    assert result["socIsBelowLimit"] is False
    place, charger = result["waypoints"]
    assert place == {  # an identical snapped location is not surfaced
        "type": "place",
        "latitude": 33.1,
        "longitude": -80.1,
        "status": "next_stop",
        "name": "Store",
        "stopDuration": 0.0,
        "stateOfCharge": 0.0,
        "rangeRemaining": 0.0,
        "arrivalTime": epoch(1790554000_000),
    }
    assert charger["type"] == "chargingStop"
    assert charger["stationId"] == "100103"
    assert charger["chargeDuration"] == 1800.0
    assert charger["arrivalTime"] == epoch(1790556200_000)
    assert charger["departureTime"] == epoch(1790558000_000)
    assert charger["compatible"] is True
    assert charger["status"] == "future"
    assert result["legs"] == [
        {
            "distance": 500.0,
            "duration": 0.0,
            "polyline": "poly",
            "energyConsumption": {
                "total": 2500.0,
                "thermal": 0.0,
                "lv": 0.0,
                "hvac": 300.0,
                "elevation": 0.0,
            },
            "trafficBlocks": [
                {
                    "firstIndex": 1,
                    "firstIndexFraction": 0.5,
                    "lastIndex": 4,
                    "lastIndexFraction": 0.25,
                    "priority": 1,
                }
            ],
            "incidents": [{"firstIndex": 3, "lastIndex": 9, "type": "construction"}],
        }
    ]
    assert result["overviewPolyline"] == "overview"
    assert result["currentArrivalSoc"] == 15.0
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
    """ETAs, the next stop, remaining distance, and the live location fix."""
    result = decode(
        "navigation.navigation_service.trip_progress",
        nav.TripProgress(
            next_waypoint=nav.Timestamp(seconds=1790553420),
            next_stop_index=1,
            distance_remaining=54.0,
            location_fix=nav.GpsFix(
                location=nav.GeoCoordinate(latitude=33.4, longitude=-80.8),
                speed=10.5,
                time=1790553428211,
            ),
        ),
    )
    assert result == {
        "nextWaypointArrivalTime": epoch(1790553420_000),
        "nextStopIndex": 1,
        "distanceRemaining": 54.0,
        "durationRemaining": 0.0,
        "latitude": 33.4,
        "longitude": -80.8,
        "speed": 10.5,
        "bearing": 0.0,
        "locationTime": epoch(1790553428211),
    }
