from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentState(_message.Message):
    __slots__ = ("deployment",)
    class SoftwareCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOFTWARE_CATEGORY_UNSPECIFIED: _ClassVar[DeploymentState.SoftwareCategory]
        SOFTWARE_CATEGORY_FIRMWARE: _ClassVar[DeploymentState.SoftwareCategory]
        SOFTWARE_CATEGORY_HD_MAPS: _ClassVar[DeploymentState.SoftwareCategory]
        SOFTWARE_CATEGORY_VEHICLE_CONFIG: _ClassVar[DeploymentState.SoftwareCategory]
    SOFTWARE_CATEGORY_UNSPECIFIED: DeploymentState.SoftwareCategory
    SOFTWARE_CATEGORY_FIRMWARE: DeploymentState.SoftwareCategory
    SOFTWARE_CATEGORY_HD_MAPS: DeploymentState.SoftwareCategory
    SOFTWARE_CATEGORY_VEHICLE_CONFIG: DeploymentState.SoftwareCategory
    class DeploymentIntent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEPLOYMENT_INTENT_UNSPECIFIED: _ClassVar[DeploymentState.DeploymentIntent]
        DEPLOYMENT_INTENT_PERFORMANCE_UPGRADE: _ClassVar[DeploymentState.DeploymentIntent]
        DEPLOYMENT_INTENT_BUG_FIX: _ClassVar[DeploymentState.DeploymentIntent]
        DEPLOYMENT_INTENT_SECURITY_UPDATE: _ClassVar[DeploymentState.DeploymentIntent]
        DEPLOYMENT_INTENT_FEATURE_ADDITION: _ClassVar[DeploymentState.DeploymentIntent]
    DEPLOYMENT_INTENT_UNSPECIFIED: DeploymentState.DeploymentIntent
    DEPLOYMENT_INTENT_PERFORMANCE_UPGRADE: DeploymentState.DeploymentIntent
    DEPLOYMENT_INTENT_BUG_FIX: DeploymentState.DeploymentIntent
    DEPLOYMENT_INTENT_SECURITY_UPDATE: DeploymentState.DeploymentIntent
    DEPLOYMENT_INTENT_FEATURE_ADDITION: DeploymentState.DeploymentIntent
    class CurrentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CURRENT_STATUS_UNSPECIFIED: _ClassVar[DeploymentState.CurrentStatus]
        CURRENT_STATUS_INSTALL_SUCCESS: _ClassVar[DeploymentState.CurrentStatus]
        CURRENT_STATUS_INSTALL_FAILED: _ClassVar[DeploymentState.CurrentStatus]
        CURRENT_STATUS_INSTALL_UNABLE_TO_START: _ClassVar[DeploymentState.CurrentStatus]
    CURRENT_STATUS_UNSPECIFIED: DeploymentState.CurrentStatus
    CURRENT_STATUS_INSTALL_SUCCESS: DeploymentState.CurrentStatus
    CURRENT_STATUS_INSTALL_FAILED: DeploymentState.CurrentStatus
    CURRENT_STATUS_INSTALL_UNABLE_TO_START: DeploymentState.CurrentStatus
    class OtaPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OTA_PHASE_UNSPECIFIED: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_IDLE: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_READY_TO_DOWNLOAD: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_FAULT: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_CONNECTION_LOST: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_INSTALL_COUNTDOWN: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_PREPARING: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_DOWNLOADING: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_READY_TO_INSTALL: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_SCHEDULED_TO_INSTALL: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_AWAITING_INSTALL: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_INSTALLING: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_INSTALL_SUCCESS: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_DOWNLOAD_FAILED: _ClassVar[DeploymentState.OtaPhase]
        OTA_PHASE_INSTALL_FAILED: _ClassVar[DeploymentState.OtaPhase]
    OTA_PHASE_UNSPECIFIED: DeploymentState.OtaPhase
    OTA_PHASE_IDLE: DeploymentState.OtaPhase
    OTA_PHASE_READY_TO_DOWNLOAD: DeploymentState.OtaPhase
    OTA_PHASE_FAULT: DeploymentState.OtaPhase
    OTA_PHASE_CONNECTION_LOST: DeploymentState.OtaPhase
    OTA_PHASE_INSTALL_COUNTDOWN: DeploymentState.OtaPhase
    OTA_PHASE_PREPARING: DeploymentState.OtaPhase
    OTA_PHASE_DOWNLOADING: DeploymentState.OtaPhase
    OTA_PHASE_READY_TO_INSTALL: DeploymentState.OtaPhase
    OTA_PHASE_SCHEDULED_TO_INSTALL: DeploymentState.OtaPhase
    OTA_PHASE_AWAITING_INSTALL: DeploymentState.OtaPhase
    OTA_PHASE_INSTALLING: DeploymentState.OtaPhase
    OTA_PHASE_INSTALL_SUCCESS: DeploymentState.OtaPhase
    OTA_PHASE_DOWNLOAD_FAILED: DeploymentState.OtaPhase
    OTA_PHASE_INSTALL_FAILED: DeploymentState.OtaPhase
    class Deployment(_message.Message):
        __slots__ = ("software_category", "version", "deployment_id", "progress_wrapper")
        SOFTWARE_CATEGORY_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_WRAPPER_FIELD_NUMBER: _ClassVar[int]
        software_category: DeploymentState.SoftwareCategory
        version: DeploymentState.Version
        deployment_id: str
        progress_wrapper: DeploymentState.ProgressWrapper
        def __init__(self, software_category: _Optional[_Union[DeploymentState.SoftwareCategory, str]] = ..., version: _Optional[_Union[DeploymentState.Version, _Mapping]] = ..., deployment_id: _Optional[str] = ..., progress_wrapper: _Optional[_Union[DeploymentState.ProgressWrapper, _Mapping]] = ...) -> None: ...
    class Version(_message.Message):
        __slots__ = ("version_string", "software_version_id", "version_year", "version_build", "version_number", "build_id")
        VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
        SOFTWARE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
        VERSION_YEAR_FIELD_NUMBER: _ClassVar[int]
        VERSION_BUILD_FIELD_NUMBER: _ClassVar[int]
        VERSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
        BUILD_ID_FIELD_NUMBER: _ClassVar[int]
        version_string: str
        software_version_id: str
        version_year: int
        version_build: int
        version_number: int
        build_id: str
        def __init__(self, version_string: _Optional[str] = ..., software_version_id: _Optional[str] = ..., version_year: _Optional[int] = ..., version_build: _Optional[int] = ..., version_number: _Optional[int] = ..., build_id: _Optional[str] = ...) -> None: ...
    class ProgressWrapper(_message.Message):
        __slots__ = ("deployment_id", "target_version", "ota_type", "deployment_context", "progress", "install_time", "install_tod", "skip_count", "skip_allowed", "deployment_intent", "is_active")
        class DeploymentContext(_message.Message):
            __slots__ = ("download_policy",)
            DOWNLOAD_POLICY_FIELD_NUMBER: _ClassVar[int]
            download_policy: int
            def __init__(self, download_policy: _Optional[int] = ...) -> None: ...
        DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
        TARGET_VERSION_FIELD_NUMBER: _ClassVar[int]
        OTA_TYPE_FIELD_NUMBER: _ClassVar[int]
        DEPLOYMENT_CONTEXT_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_FIELD_NUMBER: _ClassVar[int]
        INSTALL_TIME_FIELD_NUMBER: _ClassVar[int]
        INSTALL_TOD_FIELD_NUMBER: _ClassVar[int]
        SKIP_COUNT_FIELD_NUMBER: _ClassVar[int]
        SKIP_ALLOWED_FIELD_NUMBER: _ClassVar[int]
        DEPLOYMENT_INTENT_FIELD_NUMBER: _ClassVar[int]
        IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
        deployment_id: str
        target_version: DeploymentState.Version
        ota_type: int
        deployment_context: DeploymentState.ProgressWrapper.DeploymentContext
        progress: DeploymentState.Progress
        install_time: int
        install_tod: int
        skip_count: int
        skip_allowed: bool
        deployment_intent: DeploymentState.DeploymentIntent
        is_active: bool
        def __init__(self, deployment_id: _Optional[str] = ..., target_version: _Optional[_Union[DeploymentState.Version, _Mapping]] = ..., ota_type: _Optional[int] = ..., deployment_context: _Optional[_Union[DeploymentState.ProgressWrapper.DeploymentContext, _Mapping]] = ..., progress: _Optional[_Union[DeploymentState.Progress, _Mapping]] = ..., install_time: _Optional[int] = ..., install_tod: _Optional[int] = ..., skip_count: _Optional[int] = ..., skip_allowed: bool = ..., deployment_intent: _Optional[_Union[DeploymentState.DeploymentIntent, str]] = ..., is_active: bool = ...) -> None: ...
    class Progress(_message.Message):
        __slots__ = ("phase", "current_status", "download_progress", "install_progress", "pending_reasons", "time_remaining", "install_ready", "status_acknowledge", "install_duration")
        class Progress100(_message.Message):
            __slots__ = ("started_at", "progress_percent")
            STARTED_AT_FIELD_NUMBER: _ClassVar[int]
            PROGRESS_PERCENT_FIELD_NUMBER: _ClassVar[int]
            started_at: DeploymentState.Progress.Timestamp
            progress_percent: int
            def __init__(self, started_at: _Optional[_Union[DeploymentState.Progress.Timestamp, _Mapping]] = ..., progress_percent: _Optional[int] = ...) -> None: ...
        class Timestamp(_message.Message):
            __slots__ = ("seconds", "nanos")
            SECONDS_FIELD_NUMBER: _ClassVar[int]
            NANOS_FIELD_NUMBER: _ClassVar[int]
            seconds: int
            nanos: int
            def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
        class PendingReasons(_message.Message):
            __slots__ = ("active_mode", "fast_charging", "hv_batt_low", "lv_batt", "lv_temp_low", "not_parked", "other", "transport", "unplugged", "camp_mode")
            ACTIVE_MODE_FIELD_NUMBER: _ClassVar[int]
            FAST_CHARGING_FIELD_NUMBER: _ClassVar[int]
            HV_BATT_LOW_FIELD_NUMBER: _ClassVar[int]
            LV_BATT_FIELD_NUMBER: _ClassVar[int]
            LV_TEMP_LOW_FIELD_NUMBER: _ClassVar[int]
            NOT_PARKED_FIELD_NUMBER: _ClassVar[int]
            OTHER_FIELD_NUMBER: _ClassVar[int]
            TRANSPORT_FIELD_NUMBER: _ClassVar[int]
            UNPLUGGED_FIELD_NUMBER: _ClassVar[int]
            CAMP_MODE_FIELD_NUMBER: _ClassVar[int]
            active_mode: bool
            fast_charging: bool
            hv_batt_low: bool
            lv_batt: bool
            lv_temp_low: bool
            not_parked: bool
            other: bool
            transport: bool
            unplugged: bool
            camp_mode: bool
            def __init__(self, active_mode: bool = ..., fast_charging: bool = ..., hv_batt_low: bool = ..., lv_batt: bool = ..., lv_temp_low: bool = ..., not_parked: bool = ..., other: bool = ..., transport: bool = ..., unplugged: bool = ..., camp_mode: bool = ...) -> None: ...
        PHASE_FIELD_NUMBER: _ClassVar[int]
        CURRENT_STATUS_FIELD_NUMBER: _ClassVar[int]
        DOWNLOAD_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        INSTALL_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        PENDING_REASONS_FIELD_NUMBER: _ClassVar[int]
        TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
        INSTALL_READY_FIELD_NUMBER: _ClassVar[int]
        STATUS_ACKNOWLEDGE_FIELD_NUMBER: _ClassVar[int]
        INSTALL_DURATION_FIELD_NUMBER: _ClassVar[int]
        phase: DeploymentState.OtaPhase
        current_status: DeploymentState.CurrentStatus
        download_progress: DeploymentState.Progress.Progress100
        install_progress: DeploymentState.Progress.Progress100
        pending_reasons: DeploymentState.Progress.PendingReasons
        time_remaining: int
        install_ready: bool
        status_acknowledge: int
        install_duration: int
        def __init__(self, phase: _Optional[_Union[DeploymentState.OtaPhase, str]] = ..., current_status: _Optional[_Union[DeploymentState.CurrentStatus, str]] = ..., download_progress: _Optional[_Union[DeploymentState.Progress.Progress100, _Mapping]] = ..., install_progress: _Optional[_Union[DeploymentState.Progress.Progress100, _Mapping]] = ..., pending_reasons: _Optional[_Union[DeploymentState.Progress.PendingReasons, _Mapping]] = ..., time_remaining: _Optional[int] = ..., install_ready: bool = ..., status_acknowledge: _Optional[int] = ..., install_duration: _Optional[int] = ...) -> None: ...
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: _containers.RepeatedCompositeFieldContainer[DeploymentState.Deployment]
    def __init__(self, deployment: _Optional[_Iterable[_Union[DeploymentState.Deployment, _Mapping]]] = ...) -> None: ...

class OtaConfig(_message.Message):
    __slots__ = ("schedule", "updated_at")
    class Schedule(_message.Message):
        __slots__ = ("id", "enabled", "repeats_daily", "single_occurrence")
        ID_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        REPEATS_DAILY_FIELD_NUMBER: _ClassVar[int]
        SINGLE_OCCURRENCE_FIELD_NUMBER: _ClassVar[int]
        id: str
        enabled: bool
        repeats_daily: OtaConfig.RepeatsDaily
        single_occurrence: OtaConfig.SingleOccurrence
        def __init__(self, id: _Optional[str] = ..., enabled: bool = ..., repeats_daily: _Optional[_Union[OtaConfig.RepeatsDaily, _Mapping]] = ..., single_occurrence: _Optional[_Union[OtaConfig.SingleOccurrence, _Mapping]] = ...) -> None: ...
    class RepeatsDaily(_message.Message):
        __slots__ = ("starts_at", "location")
        STARTS_AT_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        starts_at: int
        location: OtaConfig.Location
        def __init__(self, starts_at: _Optional[int] = ..., location: _Optional[_Union[OtaConfig.Location, _Mapping]] = ...) -> None: ...
    class Location(_message.Message):
        __slots__ = ("name",)
        NAME_FIELD_NUMBER: _ClassVar[int]
        name: str
        def __init__(self, name: _Optional[str] = ...) -> None: ...
    class SingleOccurrence(_message.Message):
        __slots__ = ("starts_at",)
        class StartsAt(_message.Message):
            __slots__ = ("seconds",)
            SECONDS_FIELD_NUMBER: _ClassVar[int]
            seconds: int
            def __init__(self, seconds: _Optional[int] = ...) -> None: ...
        STARTS_AT_FIELD_NUMBER: _ClassVar[int]
        starts_at: OtaConfig.SingleOccurrence.StartsAt
        def __init__(self, starts_at: _Optional[_Union[OtaConfig.SingleOccurrence.StartsAt, _Mapping]] = ...) -> None: ...
    class UpdatedAt(_message.Message):
        __slots__ = ("seconds", "nanos")
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        NANOS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        nanos: int
        def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    schedule: _containers.RepeatedCompositeFieldContainer[OtaConfig.Schedule]
    updated_at: OtaConfig.UpdatedAt
    def __init__(self, schedule: _Optional[_Iterable[_Union[OtaConfig.Schedule, _Mapping]]] = ..., updated_at: _Optional[_Union[OtaConfig.UpdatedAt, _Mapping]] = ...) -> None: ...

class VehicleOtaState(_message.Message):
    __slots__ = ("name", "scheduled_install")
    class ScheduledInstall(_message.Message):
        __slots__ = ("seconds",)
        SECONDS_FIELD_NUMBER: _ClassVar[int]
        seconds: int
        def __init__(self, seconds: _Optional[int] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_INSTALL_FIELD_NUMBER: _ClassVar[int]
    name: str
    scheduled_install: VehicleOtaState.ScheduledInstall
    def __init__(self, name: _Optional[str] = ..., scheduled_install: _Optional[_Union[VehicleOtaState.ScheduledInstall, _Mapping]] = ...) -> None: ...
