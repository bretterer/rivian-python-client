from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HolidayCelebrationEnabled(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CarCostumeSettings(_message.Message):
    __slots__ = ("field_1", "field_2", "field_3", "field_6", "field_7", "field_9", "field_11", "field_12")
    FIELD_1_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    FIELD_6_FIELD_NUMBER: _ClassVar[int]
    FIELD_7_FIELD_NUMBER: _ClassVar[int]
    FIELD_9_FIELD_NUMBER: _ClassVar[int]
    FIELD_11_FIELD_NUMBER: _ClassVar[int]
    FIELD_12_FIELD_NUMBER: _ClassVar[int]
    field_1: int
    field_2: int
    field_3: int
    field_6: int
    field_7: int
    field_9: int
    field_11: int
    field_12: int
    def __init__(self, field_1: _Optional[int] = ..., field_2: _Optional[int] = ..., field_3: _Optional[int] = ..., field_6: _Optional[int] = ..., field_7: _Optional[int] = ..., field_9: _Optional[int] = ..., field_11: _Optional[int] = ..., field_12: _Optional[int] = ...) -> None: ...

class CarCostumeState(_message.Message):
    __slots__ = ("costume_id", "field_2", "field_3", "field_6")
    COSTUME_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    FIELD_6_FIELD_NUMBER: _ClassVar[int]
    costume_id: int
    field_2: int
    field_3: int
    field_6: int
    def __init__(self, costume_id: _Optional[int] = ..., field_2: _Optional[int] = ..., field_3: _Optional[int] = ..., field_6: _Optional[int] = ...) -> None: ...

class HalloweenCelebrationSettings(_message.Message):
    __slots__ = ("field_1", "field_2", "field_3", "field_4", "field_5", "field_7", "field_8", "field_9", "field_10", "field_11", "field_12")
    class Value(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: int
        def __init__(self, value: _Optional[int] = ...) -> None: ...
    FIELD_1_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    FIELD_3_FIELD_NUMBER: _ClassVar[int]
    FIELD_4_FIELD_NUMBER: _ClassVar[int]
    FIELD_5_FIELD_NUMBER: _ClassVar[int]
    FIELD_7_FIELD_NUMBER: _ClassVar[int]
    FIELD_8_FIELD_NUMBER: _ClassVar[int]
    FIELD_9_FIELD_NUMBER: _ClassVar[int]
    FIELD_10_FIELD_NUMBER: _ClassVar[int]
    FIELD_11_FIELD_NUMBER: _ClassVar[int]
    FIELD_12_FIELD_NUMBER: _ClassVar[int]
    field_1: HalloweenCelebrationSettings.Value
    field_2: HalloweenCelebrationSettings.Value
    field_3: HalloweenCelebrationSettings.Value
    field_4: HalloweenCelebrationSettings.Value
    field_5: HalloweenCelebrationSettings.Value
    field_7: HalloweenCelebrationSettings.Value
    field_8: HalloweenCelebrationSettings.Value
    field_9: HalloweenCelebrationSettings.Value
    field_10: HalloweenCelebrationSettings.Value
    field_11: HalloweenCelebrationSettings.Value
    field_12: HalloweenCelebrationSettings.Value
    def __init__(self, field_1: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_2: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_3: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_4: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_5: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_7: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_8: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_9: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_10: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_11: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ..., field_12: _Optional[_Union[HalloweenCelebrationSettings.Value, _Mapping]] = ...) -> None: ...
