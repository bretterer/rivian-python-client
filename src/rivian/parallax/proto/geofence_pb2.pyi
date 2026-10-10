from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeofenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GEOFENCE_TYPE_CUSTOM: _ClassVar[GeofenceType]
    GEOFENCE_TYPE_HOME: _ClassVar[GeofenceType]
    GEOFENCE_TYPE_WORK: _ClassVar[GeofenceType]
GEOFENCE_TYPE_CUSTOM: GeofenceType
GEOFENCE_TYPE_HOME: GeofenceType
GEOFENCE_TYPE_WORK: GeofenceType

class FavoriteGeofences(_message.Message):
    __slots__ = ("geofence",)
    class Geofence(_message.Message):
        __slots__ = ("type", "name")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        type: GeofenceType
        name: str
        def __init__(self, type: _Optional[_Union[GeofenceType, str]] = ..., name: _Optional[str] = ...) -> None: ...
    GEOFENCE_FIELD_NUMBER: _ClassVar[int]
    geofence: _containers.RepeatedCompositeFieldContainer[FavoriteGeofences.Geofence]
    def __init__(self, geofence: _Optional[_Iterable[_Union[FavoriteGeofences.Geofence, _Mapping]]] = ...) -> None: ...
