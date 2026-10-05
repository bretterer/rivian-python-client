"""Decoders for `geofence.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import geofence_pb2

_GEOFENCE_TYPE_MAP: Final[dict[int, str]] = {
    geofence_pb2.GEOFENCE_TYPE_HOME: "home",
    geofence_pb2.GEOFENCE_TYPE_WORK: "work",
    geofence_pb2.GEOFENCE_TYPE_CUSTOM: "custom",
}


@RVMDecoder.register(
    "geofence.geofence_service.favoriteGeofences", geofence_pb2.FavoriteGeofences
)
def decode_favorite_geofences(m: geofence_pb2.FavoriteGeofences) -> dict[str, Any]:
    """geofence.geofence_service.favoriteGeofences — saved places.

    Fields:
        favoriteGeofences: list[dict]:
            name: str — a name (e.g. "Home") or street address
            type: str ("home" | "work" | "custom")
    """
    places = []
    for geofence in m.geofence:
        place: dict[str, Any] = {}
        if (v := _present(geofence, "name")) is not None:
            place["name"] = v
        place["type"] = _enum(_GEOFENCE_TYPE_MAP, geofence.type, what="geofence type")
        places.append(place)
    return {"favoriteGeofences": places}
