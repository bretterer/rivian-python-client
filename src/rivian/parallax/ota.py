"""Decoders for `ota.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from ..utils import from_epoch
from .core import RVMDecoder, _enum, _present
from .proto import ota_pb2

_OTA_STATUS_MAP: Final[dict[int, str]] = {
    1: "idle",
    5: "install_countdown",
    6: "preparing",
    7: "downloading",
    8: "scheduled_to_install",
    10: "awaiting_install",
    11: "installing",
    12: "install_success",
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
        deploymentState: int — unknown
        otaUpdateInProgress: bool
        otaDeploymentId: str — UUID, only while an update is in flight
        otaAvailableVersion, otaAvailableVersionYear,
        otaAvailableVersionWeek, otaAvailableVersionNumber,
        otaAvailableVersionGitHash — the version being installed
        otaStatus: str — "idle" | "downloading" | "preparing" |
            "scheduled_to_install" | "install_countdown" |
            "awaiting_install" | "installing" | "install_success"
        otaDownloadProgress, otaInstallProgress: int (0-100)
        otaTimeRemaining: int (seconds; counts down during
            "install_countdown", a static default otherwise)
        otaUpdateCycleCount: int — increments when an update completes
        _otaProgressActiveFlag, _otaProgressTimeoutBudget,
        _otaProgressLateStageFlag, _otaProgressField9: int — unknown
    """
    result: dict[str, Any] = {}
    if not m.HasField("deployment"):
        return result
    deployment = m.deployment
    if (v := _present(deployment, "state")) is not None:
        result["deploymentState"] = v
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
    for field, key in (
        ("active_flag", "_otaProgressActiveFlag"),
        ("timeout_budget", "_otaProgressTimeoutBudget"),
        ("late_stage_flag", "_otaProgressLateStageFlag"),
    ):
        if (v := _present(wrapper, field)) is not None:
            result[key] = v

    if not wrapper.HasField("progress"):
        return result
    progress = wrapper.progress
    if (v := _present(progress, "phase")) is not None:
        result["otaStatus"] = _enum(_OTA_STATUS_MAP, v, what="OTA status")
    if (
        progress.HasField("download_progress")
        and (v := _present(progress.download_progress, "field_2")) is not None
    ):
        result["otaDownloadProgress"] = v
    if (
        progress.HasField("install_progress")
        and (v := _present(progress.install_progress, "field_2")) is not None
    ):
        result["otaInstallProgress"] = v
    for field, key in (
        ("time_remaining", "otaTimeRemaining"),
        ("update_cycle_count", "otaUpdateCycleCount"),
        ("field_9", "_otaProgressField9"),
    ):
        if (v := _present(progress, field)) is not None:
            result[key] = v
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
        one_time = schedule.HasField("one_time")
        entry: dict[str, Any] = {"type": "one_time" if one_time else "recurring"}
        if (v := _present(schedule, "id")) is not None:
            entry["id"] = v
        if schedule.HasField("time_of_day"):
            time_of_day = schedule.time_of_day
            if (v := _present(time_of_day, "start_time")) is not None:
                entry["startTime"] = v
            if (
                time_of_day.HasField("location")
                and (v := _present(time_of_day.location, "name")) is not None
            ):
                entry["location"] = v
        if one_time and (
            seconds := _present(schedule.one_time.install_time, "seconds")
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
def decode_vehicle_ota_state(_m: ota_pb2.VehicleOtaState) -> dict[str, Any]:
    """ota.ota_state.vehicle_ota_state — sent when OTA settings change; no data."""
    return {}
