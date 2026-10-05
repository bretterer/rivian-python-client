from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CostumeEffectTrigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COSTUME_EFFECT_TRIGGER_UNSPECIFIED: _ClassVar[CostumeEffectTrigger]
    COSTUME_EFFECT_TRIGGER_MANUAL: _ClassVar[CostumeEffectTrigger]
    COSTUME_EFFECT_TRIGGER_MOTION: _ClassVar[CostumeEffectTrigger]
COSTUME_EFFECT_TRIGGER_UNSPECIFIED: CostumeEffectTrigger
COSTUME_EFFECT_TRIGGER_MANUAL: CostumeEffectTrigger
COSTUME_EFFECT_TRIGGER_MOTION: CostumeEffectTrigger

class HolidayCelebrationEnabled(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CarCostumeSettings(_message.Message):
    __slots__ = ("celebration_sound_volume", "interior_music_enabled", "interior_music_type", "motion_exterior_light_sound_effect", "interior_light_show_enabled", "interior_overhead_lights_enabled", "lights_color", "costume_effect", "effect_trigger")
    CELEBRATION_SOUND_VOLUME_FIELD_NUMBER: _ClassVar[int]
    INTERIOR_MUSIC_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INTERIOR_MUSIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    MOTION_EXTERIOR_LIGHT_SOUND_EFFECT_FIELD_NUMBER: _ClassVar[int]
    INTERIOR_LIGHT_SHOW_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INTERIOR_OVERHEAD_LIGHTS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LIGHTS_COLOR_FIELD_NUMBER: _ClassVar[int]
    COSTUME_EFFECT_FIELD_NUMBER: _ClassVar[int]
    EFFECT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    celebration_sound_volume: int
    interior_music_enabled: bool
    interior_music_type: int
    motion_exterior_light_sound_effect: int
    interior_light_show_enabled: bool
    interior_overhead_lights_enabled: bool
    lights_color: int
    costume_effect: int
    effect_trigger: CostumeEffectTrigger
    def __init__(self, celebration_sound_volume: _Optional[int] = ..., interior_music_enabled: bool = ..., interior_music_type: _Optional[int] = ..., motion_exterior_light_sound_effect: _Optional[int] = ..., interior_light_show_enabled: bool = ..., interior_overhead_lights_enabled: bool = ..., lights_color: _Optional[int] = ..., costume_effect: _Optional[int] = ..., effect_trigger: _Optional[_Union[CostumeEffectTrigger, str]] = ...) -> None: ...

class CarCostumeState(_message.Message):
    __slots__ = ("car_costume_availability", "costume_theme", "motion_trigger_detected", "costume_start_time", "active_costume_effect")
    class Timestamp(_message.Message):
        __slots__ = ("seconds", "nanos")
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        NANOS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        nanos: int
        def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
    CAR_COSTUME_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    COSTUME_THEME_FIELD_NUMBER: _ClassVar[int]
    MOTION_TRIGGER_DETECTED_FIELD_NUMBER: _ClassVar[int]
    COSTUME_START_TIME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_COSTUME_EFFECT_FIELD_NUMBER: _ClassVar[int]
    car_costume_availability: int
    costume_theme: int
    motion_trigger_detected: bool
    costume_start_time: CarCostumeState.Timestamp
    active_costume_effect: int
    def __init__(self, car_costume_availability: _Optional[int] = ..., costume_theme: _Optional[int] = ..., motion_trigger_detected: bool = ..., costume_start_time: _Optional[_Union[CarCostumeState.Timestamp, _Mapping]] = ..., active_costume_effect: _Optional[int] = ...) -> None: ...

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
    lights_color: HalloweenCelebrationSettings.Int32Value
    car_costume_availability: HalloweenCelebrationSettings.StringValue
    motion_light_sound_enabled: bool
    def __init__(self, costume_theme: _Optional[_Union[HalloweenCelebrationSettings.CostumeTheme, _Mapping]] = ..., sound_volume: _Optional[_Union[HalloweenCelebrationSettings.Int32Value, _Mapping]] = ..., music_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., music_type: _Optional[_Union[HalloweenCelebrationSettings.Int32Value, _Mapping]] = ..., sound_effect: _Optional[_Union[HalloweenCelebrationSettings.StringValue, _Mapping]] = ..., exterior_sound_effect: _Optional[int] = ..., exterior_sounds_muted: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., light_show_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., interior_overhead_lights_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., exterior_light_show_enabled: _Optional[_Union[HalloweenCelebrationSettings.BoolValue, _Mapping]] = ..., lights_color: _Optional[_Union[HalloweenCelebrationSettings.Int32Value, _Mapping]] = ..., car_costume_availability: _Optional[_Union[HalloweenCelebrationSettings.StringValue, _Mapping]] = ..., motion_light_sound_enabled: bool = ...) -> None: ...
