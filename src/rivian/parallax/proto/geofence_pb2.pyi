from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FavoriteGeofences(_message.Message):
    __slots__ = ("geofence",)
    class Geofence(_message.Message):
        __slots__ = ("field_1", "name")
        FIELD_1_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        field_1: int
        name: str
        def __init__(self, field_1: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    GEOFENCE_FIELD_NUMBER: _ClassVar[int]
    geofence: _containers.RepeatedCompositeFieldContainer[FavoriteGeofences.Geofence]
    def __init__(self, geofence: _Optional[_Iterable[_Union[FavoriteGeofences.Geofence, _Mapping]]] = ...) -> None: ...
