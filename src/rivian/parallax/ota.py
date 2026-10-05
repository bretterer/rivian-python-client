"""Decoders for `ota.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from ..utils import from_epoch
from .core import RVMDecoder, _enum, _present
from .proto import ota_pb2

_OTA_STATUS_MAP: Final[dict[int, str]] = {
    ota_pb2.DeploymentState.OTA_PHASE_IDLE: "idle",
    ota_pb2.DeploymentState.OTA_PHASE_READY_TO_DOWNLOAD: "ready_to_download",
    ota_pb2.DeploymentState.OTA_PHASE_FAULT: "fault",
    ota_pb2.DeploymentState.OTA_PHASE_CONNECTION_LOST: "connection_lost",
    ota_pb2.DeploymentState.OTA_PHASE_INSTALL_COUNTDOWN: "install_countdown",
    ota_pb2.DeploymentState.OTA_PHASE_PREPARING: "preparing",
    ota_pb2.DeploymentState.OTA_PHASE_DOWNLOADING: "downloading",
    ota_pb2.DeploymentState.OTA_PHASE_READY_TO_INSTALL: "ready_to_install",
    ota_pb2.DeploymentState.OTA_PHASE_SCHEDULED_TO_INSTALL: "scheduled_to_install",
    ota_pb2.DeploymentState.OTA_PHASE_AWAITING_INSTALL: "awaiting_install",
    ota_pb2.DeploymentState.OTA_PHASE_INSTALLING: "installing",
    ota_pb2.DeploymentState.OTA_PHASE_INSTALL_SUCCESS: "install_success",
    ota_pb2.DeploymentState.OTA_PHASE_DOWNLOAD_FAILED: "download_failed",
    ota_pb2.DeploymentState.OTA_PHASE_INSTALL_FAILED: "install_failed",
}


_Deployment = ota_pb2.DeploymentState
# The app's GraphQL-style strings.
_CURRENT_STATUS_MAP: Final[dict[int, str]] = {
    _Deployment.CURRENT_STATUS_INSTALL_SUCCESS: "Install_Success",
    _Deployment.CURRENT_STATUS_INSTALL_FAILED: "Install_Failed",
    _Deployment.CURRENT_STATUS_INSTALL_UNABLE_TO_START: "Install_Unable_To_Start",
}

_DEPLOYMENT_INTENT_MAP: Final[dict[int, str]] = {
    _Deployment.DEPLOYMENT_INTENT_PERFORMANCE_UPGRADE: "Performance_Upgrade",
    _Deployment.DEPLOYMENT_INTENT_BUG_FIX: "Bug_Fix",
    _Deployment.DEPLOYMENT_INTENT_SECURITY_UPDATE: "Security_Update",
    _Deployment.DEPLOYMENT_INTENT_FEATURE_ADDITION: "Feature_Addition",
}

_SOFTWARE_CATEGORY_MAP: Final[dict[int, str]] = {
    _Deployment.SOFTWARE_CATEGORY_FIRMWARE: "Firmware",
    _Deployment.SOFTWARE_CATEGORY_HD_MAPS: "HD_Maps",
    _Deployment.SOFTWARE_CATEGORY_VEHICLE_CONFIG: "Vehicle_Config",
}


def _decode_version(
    version: ota_pb2.DeploymentState.Version, prefix: str
) -> dict[str, Any]:
    """Decode a Version submessage into `<prefix>Version`-style keys."""
    result: dict[str, Any] = {}
    for field, key in (
        ("version_string", "Version"),
        ("version_year", "VersionYear"),
        ("version_build", "VersionWeek"),
        ("build_id", "VersionGitHash"),
    ):
        if (v := _present(version, field)) is not None:
            result[f"{prefix}{key}"] = v
    # year.week.number
    if (
        (string := result.get(f"{prefix}Version"))
        and len(parts := string.split(".")) == 3
        and parts[2].isdigit()
    ):
        result[f"{prefix}VersionNumber"] = int(parts[2])
    return result


@RVMDecoder.register("ota.deployment.state", ota_pb2.DeploymentState)
def decode_deployment_state(m: ota_pb2.DeploymentState) -> dict[str, Any]:
    """ota.deployment.state — installed version and OTA update progress.

    Fields:
        otaCurrentVersion: str (year.week.number)
        otaCurrentVersionYear, otaCurrentVersionWeek,
            otaCurrentVersionNumber: int
        otaCurrentVersionGitHash: str
        otaSoftwareCategory: str ("Firmware" | "HD_Maps" | "Vehicle_Config")
        otaUpdateInProgress: bool
        otaDeploymentId: str — UUID, only while an update is in flight
        otaAvailableVersion, otaAvailableVersionYear,
        otaAvailableVersionWeek, otaAvailableVersionNumber,
        otaAvailableVersionGitHash — the version being installed
        otaStatus: str — "idle" | "ready_to_download" | "downloading" |
            "preparing" | "ready_to_install" | "scheduled_to_install" |
            "install_countdown" | "awaiting_install" | "installing" |
            "install_success" | "fault" | "connection_lost" |
            "download_failed" | "install_failed"
        otaDownloadProgress, otaInstallProgress: int (0-100)
        otaTimeRemaining: int (seconds; counts down during
            "install_countdown", a static default otherwise)
        otaCurrentStatus: str | None ("Install_Success" | "Install_Failed" |
            "Install_Unable_To_Start") — the last install's result
        otaInstallReady: str ("ota_available" | "ota_not_available")
        otaInstallDuration: int (minutes)
        otaInstallTimeOfDay: int (minutes after local midnight), when set
        otaDeploymentIntent: str | None ("Performance_Upgrade" | "Bug_Fix" |
            "Security_Update" | "Feature_Addition")
        otaSkipAllowed: bool, otaSkipCount: int
        otaPendingReasons: list[str] — what's blocking an install, e.g.
            "not_parked", "unplugged", "lv_batt"
        _otaType, _otaIsActive, _otaStatusAcknowledge: raw
    """
    result: dict[str, Any] = {}
    if not m.deployment:
        return result
    # Like the app, report the firmware deployment.
    deployment = next(
        (
            d
            for d in m.deployment
            if d.software_category == _Deployment.SOFTWARE_CATEGORY_FIRMWARE
        ),
        m.deployment[0],
    )
    if (v := _present(deployment, "software_category")) is not None:
        result["otaSoftwareCategory"] = _enum(
            _SOFTWARE_CATEGORY_MAP, v, what="OTA software category"
        )
    if deployment.HasField("version"):
        result.update(_decode_version(deployment.version, "otaCurrent"))

    if not deployment.HasField("progress_wrapper"):
        return result
    wrapper = deployment.progress_wrapper
    # The wrapper is always present; deployment_id is absent at rest.
    deployment_id = _present(wrapper, "deployment_id")
    result["otaUpdateInProgress"] = deployment_id is not None
    if deployment_id is not None:
        result["otaDeploymentId"] = deployment_id
    if wrapper.HasField("target_version"):
        result.update(_decode_version(wrapper.target_version, "otaAvailable"))
    if (v := _present(wrapper, "install_tod")) is not None:
        result["otaInstallTimeOfDay"] = v
    result["otaDeploymentIntent"] = _enum(
        _DEPLOYMENT_INTENT_MAP,
        wrapper.deployment_intent or None,
        what="OTA deployment intent",
    )
    result["otaSkipAllowed"] = wrapper.skip_allowed
    result["otaSkipCount"] = wrapper.skip_count
    for field, key in (("ota_type", "_otaType"), ("is_active", "_otaIsActive")):
        if (v := _present(wrapper, field)) is not None:
            result[key] = v

    if not wrapper.HasField("progress"):
        return result
    progress = wrapper.progress
    if (v := _present(progress, "phase")) is not None:
        result["otaStatus"] = _enum(_OTA_STATUS_MAP, v, what="OTA status")
    result["otaCurrentStatus"] = _enum(
        _CURRENT_STATUS_MAP, progress.current_status or None, what="OTA current status"
    )
    for field, key in (
        ("download_progress", "otaDownloadProgress"),
        ("install_progress", "otaInstallProgress"),
    ):
        if (
            progress.HasField(field)
            and (v := _present(getattr(progress, field), "progress_percent"))
            is not None
        ):
            result[key] = v
    result["otaTimeRemaining"] = progress.time_remaining
    result["otaInstallReady"] = (
        "ota_available" if progress.install_ready else "ota_not_available"
    )
    result["otaInstallDuration"] = progress.install_duration
    reasons = progress.pending_reasons
    result["otaPendingReasons"] = [
        field.name for field, value in reasons.ListFields() if value
    ]
    result["_otaStatusAcknowledge"] = progress.status_acknowledge
    return result


@RVMDecoder.register("ota.user_schedule.ota_config", ota_pb2.OtaConfig)
def decode_ota_config(m: ota_pb2.OtaConfig) -> dict[str, Any]:
    """ota.user_schedule.ota_config — install schedules.

    Fields:
        otaSchedules: list[dict] (empty when none is set), each with:
            type: str — "one_time" (a scheduled install) or "recurring"
                (auto-install)
            id: str — UUID, when sent
            enabled: bool
            installTime: datetime — one-time only, once a time is picked;
                kept after the install or a cancel
            startTime: int — recurring only; minutes after local midnight
            location: str — recurring only; a saved location (e.g.
                "home") or "anywhere"
        otaScheduleUpdatedAt: datetime
    """
    schedules: list[dict[str, Any]] = []
    for schedule in m.schedule:
        one_time = schedule.WhichOneof("occurrence") == "single_occurrence"
        entry: dict[str, Any] = {"type": "one_time" if one_time else "recurring"}
        if (v := _present(schedule, "id")) is not None:
            entry["id"] = v
        if schedule.HasField("repeats_daily"):
            daily = schedule.repeats_daily
            if (v := _present(daily, "starts_at")) is not None:
                entry["startTime"] = v
            if (
                daily.HasField("location")
                and (v := _present(daily.location, "name")) is not None
            ):
                entry["location"] = v
        if one_time and (
            seconds := _present(schedule.single_occurrence.starts_at, "seconds")
        ):
            entry["installTime"] = from_epoch(seconds)
        entry["enabled"] = schedule.enabled
        schedules.append(entry)

    result: dict[str, Any] = {"otaSchedules": schedules}
    if m.HasField("updated_at"):
        seconds = m.updated_at.seconds + m.updated_at.nanos / 1e9
        result["otaScheduleUpdatedAt"] = from_epoch(seconds)
    return result


@RVMDecoder.register("ota.ota_state.vehicle_ota_state", ota_pb2.VehicleOtaState)
def decode_vehicle_ota_state(m: ota_pb2.VehicleOtaState) -> dict[str, Any]:
    """ota.ota_state.vehicle_ota_state — the pending scheduled install.

    Fields:
        otaScheduledInstallTime: datetime | None — None when no install is
            scheduled (never set, cancelled, or already installed)
    """
    seconds = _present(m.scheduled_install, "seconds")
    return {"otaScheduledInstallTime": from_epoch(seconds) if seconds else None}
