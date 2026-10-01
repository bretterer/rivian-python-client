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
        version_build=36,
        build_id="0a1b2c3d",
    )

    idle = decode(
        "ota.deployment.state",
        deployment(
            deployment=deployment.Deployment(
                state=1,
                version=version,
                progress_wrapper=deployment.ProgressWrapper(
                    progress=deployment.Progress(phase=deployment.OTA_PHASE_IDLE)
                ),
            )
        ),
    )
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
            deployment=deployment.Deployment(
                version=version,
                progress_wrapper=deployment.ProgressWrapper(
                    deployment_id="uuid",
                    progress=deployment.Progress(
                        phase=deployment.OTA_PHASE_DOWNLOADING,
                        download_progress=deployment.Progress.Progress100(field_2=42),
                    ),
                ),
            )
        ),
    )
    assert active["otaUpdateInProgress"] is True
    assert active["otaDeploymentId"] == "uuid"
    assert active["otaStatus"] == "downloading"
    assert active["otaDownloadProgress"] == 42


def test_ota_config() -> None:
    """Schedule entries and when the schedule last changed."""
    config = ota.OtaConfig
    result = decode(
        "ota.user_schedule.ota_config",
        config(
            schedule=[
                config.Schedule(id="a", field_4=config.Unmapped4()),
                config.Schedule(
                    id="b",
                    enabled=True,
                    time_of_day=config.TimeOfDay(
                        start_time=240, location=config.Location(name="home")
                    ),
                ),
            ],
            updated_at=config.UpdatedAt(seconds=1723681179, nanos=500_000_000),
        ),
    )
    assert result == {
        "otaSchedules": [
            {"id": "a", "enabled": False, "_field4": ""},
            {"id": "b", "enabled": True, "startTime": 240, "location": "home"},
        ],
        "otaScheduleUpdatedAt": epoch(1723681179_500),
    }


def test_ota_config_empty() -> None:
    """No schedule configured reads as an empty list."""
    assert decode("ota.user_schedule.ota_config") == {"otaSchedules": []}
