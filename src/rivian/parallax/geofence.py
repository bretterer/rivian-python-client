"""Decoders for `geofence.*` RVM topics."""

from __future__ import annotations

from typing import Any

from .core import RVMDecoder, _present
from .proto import geofence_pb2


@RVMDecoder.register(
    "geofence.geofence_service.favoriteGeofences", geofence_pb2.FavoriteGeofences
)
def decode_favorite_geofences(m: geofence_pb2.FavoriteGeofences) -> dict[str, Any]:
    """geofence.geofence_service.favoriteGeofences — saved places.

    Fields:
        favoriteGeofences: list[dict]:
            name: str — a name (e.g. "Home") or street address
            _field1: int, when sent — unknown (1 only on "Home")
    """
    places = []
    for geofence in m.geofence:
        place: dict[str, Any] = {}
        if (v := _present(geofence, "name")) is not None:
            place["name"] = v
        if (v := _present(geofence, "field_1")) is not None:
            place["_field1"] = v
        places.append(place)
    return {"favoriteGeofences": places}
