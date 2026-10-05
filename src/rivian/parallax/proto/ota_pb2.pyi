from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentState(_message.Message):
    __slots__ = ("deployment",)
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
        __slots__ = ("state", "version", "progress_wrapper")
        STATE_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_WRAPPER_FIELD_NUMBER: _ClassVar[int]
        state: int
        version: DeploymentState.Version
        progress_wrapper: DeploymentState.ProgressWrapper
        def __init__(self, state: _Optional[int] = ..., version: _Optional[_Union[DeploymentState.Version, _Mapping]] = ..., progress_wrapper: _Optional[_Union[DeploymentState.ProgressWrapper, _Mapping]] = ...) -> None: ...
    class Version(_message.Message):
        __slots__ = ("version_string", "version_year", "version_build", "build_id")
        VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
        VERSION_YEAR_FIELD_NUMBER: _ClassVar[int]
        VERSION_BUILD_FIELD_NUMBER: _ClassVar[int]
        BUILD_ID_FIELD_NUMBER: _ClassVar[int]
        version_string: str
        version_year: int
        version_build: int
        build_id: str
        def __init__(self, version_string: _Optional[str] = ..., version_year: _Optional[int] = ..., version_build: _Optional[int] = ..., build_id: _Optional[str] = ...) -> None: ...
    class ProgressWrapper(_message.Message):
        __slots__ = ("deployment_id", "target_version", "active_flag", "progress", "timeout_budget", "late_stage_flag")
        DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
        TARGET_VERSION_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FLAG_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_FIELD_NUMBER: _ClassVar[int]
        TIMEOUT_BUDGET_FIELD_NUMBER: _ClassVar[int]
        LATE_STAGE_FLAG_FIELD_NUMBER: _ClassVar[int]
        deployment_id: str
        target_version: DeploymentState.Version
        active_flag: int
        progress: DeploymentState.Progress
        timeout_budget: int
        late_stage_flag: int
        def __init__(self, deployment_id: _Optional[str] = ..., target_version: _Optional[_Union[DeploymentState.Version, _Mapping]] = ..., active_flag: _Optional[int] = ..., progress: _Optional[_Union[DeploymentState.Progress, _Mapping]] = ..., timeout_budget: _Optional[int] = ..., late_stage_flag: _Optional[int] = ...) -> None: ...
    class Progress(_message.Message):
        __slots__ = ("phase", "field_2", "download_progress", "install_progress", "field_5", "time_remaining", "field_7", "update_cycle_count", "field_9")
        class Progress100(_message.Message):
            __slots__ = ("field_2",)
            FIELD_2_FIELD_NUMBER: _ClassVar[int]
            field_2: int
            def __init__(self, field_2: _Optional[int] = ...) -> None: ...
        PHASE_FIELD_NUMBER: _ClassVar[int]
        FIELD_2_FIELD_NUMBER: _ClassVar[int]
        DOWNLOAD_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        INSTALL_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        FIELD_5_FIELD_NUMBER: _ClassVar[int]
        TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
        FIELD_7_FIELD_NUMBER: _ClassVar[int]
        UPDATE_CYCLE_COUNT_FIELD_NUMBER: _ClassVar[int]
        FIELD_9_FIELD_NUMBER: _ClassVar[int]
        phase: DeploymentState.OtaPhase
        field_2: int
        download_progress: DeploymentState.Progress.Progress100
        install_progress: DeploymentState.Progress.Progress100
        field_5: str
        time_remaining: int
        field_7: int
        update_cycle_count: int
        field_9: int
        def __init__(self, phase: _Optional[_Union[DeploymentState.OtaPhase, str]] = ..., field_2: _Optional[int] = ..., download_progress: _Optional[_Union[DeploymentState.Progress.Progress100, _Mapping]] = ..., install_progress: _Optional[_Union[DeploymentState.Progress.Progress100, _Mapping]] = ..., field_5: _Optional[str] = ..., time_remaining: _Optional[int] = ..., field_7: _Optional[int] = ..., update_cycle_count: _Optional[int] = ..., field_9: _Optional[int] = ...) -> None: ...
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: DeploymentState.Deployment
    def __init__(self, deployment: _Optional[_Union[DeploymentState.Deployment, _Mapping]] = ...) -> None: ...

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
