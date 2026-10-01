"""Tests for the `geofence.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import geofence_pb2 as geofence

from .helpers import decode


def test_favorite_geofences() -> None:
    """Saved places come through by name."""
    entry = geofence.FavoriteGeofences.Geofence
    result = decode(
        "geofence.geofence_service.favoriteGeofences",
        geofence.FavoriteGeofences(
            geofence=[entry(field_1=1, name="Home"), entry(name="123 Main St")]
        ),
    )
    assert result == {
        "favoriteGeofences": [{"name": "Home", "_field1": 1}, {"name": "123 Main St"}]
    }
