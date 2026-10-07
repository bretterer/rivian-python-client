"""Tests for the `ota.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import ota_pb2 as ota

from .helpers import decode, epoch


def test_ota_deployment_state() -> None:
    """Installed version, and progress only counting as in-flight with an id."""
    deployment = ota.DeploymentState
    version = deployment.Version(
        version_string="2026.36.1",
        version_year=2026,
        version_week=36,
        git_hash="0a1b2c3d",
    )

    idle = decode(
        "ota.deployment.state",
        deployment(
            deployment=[
                deployment.Deployment(
                    software_category=deployment.SOFTWARE_CATEGORY_FIRMWARE,
                    version=version,
                    progress_wrapper=deployment.ProgressWrapper(
                        progress=deployment.Progress(phase=deployment.OTA_PHASE_IDLE)
                    ),
                )
            ]
        ),
    )
    assert idle["otaSoftwareCategory"] == "Firmware"
    assert idle["otaCurrentVersion"] == "2026.36.1"
    assert idle["otaCurrentVersionYear"] == 2026
    assert idle["otaCurrentVersionWeek"] == 36
    assert idle["otaCurrentVersionNumber"] == 1
    assert idle["otaCurrentVersionGitHash"] == "0a1b2c3d"
    assert idle["otaUpdateInProgress"] is False
    assert idle["otaStatus"] == "idle"

    active = decode(
        "ota.deployment.state",
        deployment(
            deployment=[
                deployment.Deployment(
                    version=version,
                    progress_wrapper=deployment.ProgressWrapper(
                        deployment_id="uuid",
                        progress=deployment.Progress(
                            phase=deployment.OTA_PHASE_DOWNLOADING,
                            download_progress=deployment.Progress.Progress100(
                                progress_percent=42
                            ),
                        ),
                    ),
                )
            ]
        ),
    )
    assert active["otaUpdateInProgress"] is True
    assert active["otaDeploymentId"] == "uuid"
    assert active["otaStatus"] == "downloading"
    assert active["otaDownloadProgress"] == 42
    assert active["otaInstallReady"] == "ota_not_available"
    assert active["otaPendingReasons"] == []


def test_ota_progress_details() -> None:
    """Install readiness, result, duration, blockers and intent."""
    deployment = ota.DeploymentState
    progress = deployment.Progress
    result = decode(
        "ota.deployment.state",
        deployment(
            deployment=[
                deployment.Deployment(
                    progress_wrapper=deployment.ProgressWrapper(
                        install_tod=180,
                        deployment_intent=deployment.DEPLOYMENT_INTENT_BUG_FIX,
                        progress=progress(
                            phase=deployment.OTA_PHASE_READY_TO_INSTALL,
                            current_status=deployment.CURRENT_STATUS_INSTALL_SUCCESS,
                            install_ready=True,
                            install_duration=50,
                            pending_reasons=progress.PendingReasons(
                                not_parked=True, unplugged=True
                            ),
                        ),
                    )
                )
            ]
        ),
    )
    assert result["otaInstallTimeOfDay"] == 180
    assert result["otaDeploymentIntent"] == "Bug_Fix"
    assert result["otaCurrentStatus"] == "Install_Success"
    assert result["otaInstallReady"] == "ota_available"
    assert result["otaInstallDuration"] == 50
    assert result["otaPendingReasons"] == ["not_parked", "unplugged"]


def test_ota_config() -> None:
    """Schedule entries and when the schedule last changed."""
    config = ota.OtaConfig
    result = decode(
        "ota.user_schedule.ota_config",
        config(
            schedule=[
                config.Schedule(
                    id="a",
                    enabled=True,
                    single_occurrence=config.SingleOccurrence(
                        starts_at=config.SingleOccurrence.StartsAt(seconds=1790977560)
                    ),
                ),
                config.Schedule(
                    id="b",
                    enabled=True,
                    repeats_daily=config.RepeatsDaily(
                        starts_at=240, location=config.Location(name="home")
                    ),
                ),
            ],
            updated_at=config.UpdatedAt(seconds=1723681179, nanos=500_000_000),
        ),
    )
    assert result == {
        "otaSchedules": [
            {
                "type": "one_time",
                "id": "a",
                "installTime": epoch(1790977560_000),
                "enabled": True,
            },
            {
                "type": "recurring",
                "id": "b",
                "enabled": True,
                "startTime": 240,
                "location": "home",
            },
        ],
        "otaScheduleUpdatedAt": epoch(1723681179_500),
    }


def test_ota_config_empty() -> None:
    """No schedule configured reads as an empty list."""
    assert decode("ota.user_schedule.ota_config") == {"otaSchedules": []}


def test_ota_config_one_time_without_time() -> None:
    """A one-time entry with no time picked has no installTime."""
    config = ota.OtaConfig
    result = decode(
        "ota.user_schedule.ota_config",
        config(schedule=[config.Schedule(single_occurrence=config.SingleOccurrence())]),
    )
    assert result == {"otaSchedules": [{"type": "one_time", "enabled": False}]}


def test_ota_config_one_time_sentinel_time() -> None:
    """A starts_at before the Unix epoch is a "not set" sentinel, not a time."""
    config = ota.OtaConfig
    occurrence = config.SingleOccurrence()
    occurrence.starts_at.seconds = -62135596800
    result = decode(
        "ota.user_schedule.ota_config",
        config(schedule=[config.Schedule(single_occurrence=occurrence)]),
    )
    assert result == {"otaSchedules": [{"type": "one_time", "enabled": False}]}


def test_vehicle_ota_state() -> None:
    """The pending scheduled install time, or None when nothing is scheduled."""
    state = ota.VehicleOtaState
    rvm = "ota.ota_state.vehicle_ota_state"
    scheduled = state(
        name="VehicleOTAState",
        scheduled_install=state.ScheduledInstall(seconds=1790977560),
    )
    assert decode(rvm, scheduled) == {"otaScheduledInstallTime": epoch(1790977560_000)}
    assert decode(rvm, state(name="VehicleOTAState")) == {
        "otaScheduledInstallTime": None
    }


def test_ota_deployment_state_picks_firmware() -> None:
    """With several deployments, the firmware one is reported."""
    deployment = ota.DeploymentState
    result = decode(
        "ota.deployment.state",
        deployment(
            deployment=[
                deployment.Deployment(
                    software_category=deployment.SOFTWARE_CATEGORY_HD_MAPS,
                    version=deployment.Version(version_string="2026.1.0"),
                ),
                deployment.Deployment(
                    software_category=deployment.SOFTWARE_CATEGORY_FIRMWARE,
                    version=deployment.Version(version_string="2026.36.1"),
                ),
            ]
        ),
    )
    assert result["otaSoftwareCategory"] == "Firmware"
    assert result["otaCurrentVersion"] == "2026.36.1"
