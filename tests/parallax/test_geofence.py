"""Tests for the `geofence.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import geofence_pb2 as geofence

from .helpers import decode


def test_favorite_geofences() -> None:
    """Saved places come through by name, with their type when sent."""
    entry = geofence.FavoriteGeofences.Geofence
    result = decode(
        "geofence.geofence_service.favoriteGeofences",
        geofence.FavoriteGeofences(
            geofence=[
                entry(type=geofence.GEOFENCE_TYPE_HOME, name="Home"),
                entry(type=geofence.GEOFENCE_TYPE_WORK, name="Work"),
                entry(name="123 Main St"),
            ]
        ),
    )
    assert result == {
        "favoriteGeofences": [
            {"name": "Home", "type": "home"},
            {"name": "Work", "type": "work"},
            {"name": "123 Main St"},
        ]
    }
