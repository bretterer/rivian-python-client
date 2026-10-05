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
    __slots__ = ("costume_theme", "sound_volume", "music_enabled", "music_type", "sound_effect", "exterior_sound_effect", "exterior_sounds_muted", "light_show_enabled", "interior_overhead_lights_enabled", "exterior_light_show_enabled", "lights_color", "car_costume_availability", "motion_light_sound_enabled")
    class CostumeTheme(_message.Message):
        __slots__ = ("theme_name",)
        THEME_NAME_FIELD_NUMBER: _ClassVar[int]
        theme_name: str
        def __init__(self, theme_name: _Optional[str] = ...) -> None: ...
    class BoolValue(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: bool
        def __init__(self, value: bool = ...) -> None: ...
    class Int32Value(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: int
        def __init__(self, value: _Optional[int] = ...) -> None: ...
    class StringValue(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: str
        def __init__(self, value: _Optional[str] = ...) -> None: ...
    COSTUME_THEME_FIELD_NUMBER: _ClassVar[int]
    SOUND_VOLUME_FIELD_NUMBER: _ClassVar[int]
    MUSIC_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MUSIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOUND_EFFECT_FIELD_NUMBER: _ClassVar[int]
    EXTERIOR_SOUND_EFFECT_FIELD_NUMBER: _ClassVar[int]
    EXTERIOR_SOUNDS_MUTED_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SHOW_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INTERIOR_OVERHEAD_LIGHTS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    EXTERIOR_LIGHT_SHOW_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LIGHTS_COLOR_FIELD_NUMBER: _ClassVar[int]
    CAR_COSTUME_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    MOTION_LIGHT_SOUND_ENABLED_FIELD_NUMBER: _ClassVar[int]
    costume_theme: HalloweenCelebrationSettings.CostumeTheme
    sound_volume: HalloweenCelebrationSettings.Int32Value
    music_enabled: HalloweenCelebrationSettings.BoolValue
    music_type: HalloweenCelebrationSettings.Int32Value
    sound_effect: HalloweenCelebrationSettings.StringValue
    exterior_sound_effect: int
    exterior_sounds_muted: HalloweenCelebrationSettings.BoolValue
    light_show_enabled: HalloweenCelebrationSettings.BoolValue
    interior_overhead_lights_enabled: HalloweenCelebrationSettings.BoolValue
    exterior_light_show_enabled: HalloweenCelebrationSettings.BoolValue
    lights_color: HalloweenCelebrationSettings.StringValue
    car_costume_availability: HalloweenCelebrationSettings.StringValue
    motion_light_sound_enabled: bool
    def __init__(self, costume_theme: _Optional[_Union[HalloweenCelebrationSettings.CostumeTheme, _Mapping]] = ..., sound_volume: _Optional[_Union[HalloweenCelebrationSettings.Int32Value, _Mapping]] = ..., music_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., music_type: _Optional[_Union[HalloweenCelebrationSettings.Int32Value, _Mapping]] = ..., sound_effect: _Optional[_Union[HalloweenCelebrationSettings.StringValue, _Mapping]] = ..., exterior_sound_effect: _Optional[int] = ..., exterior_sounds_muted: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., light_show_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., interior_overhead_lights_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., exterior_light_show_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., lights_color: _Optional[_Union[HalloweenCelebrationSettings.StringValue, _Mapping]] = ..., car_costume_availability: _Optional[_Union[HalloweenCelebrationSettings.StringValue, _Mapping]] = ..., motion_light_sound_enabled: bool = ...) -> None: ...
