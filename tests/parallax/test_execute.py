import asyncio
import base64
import uuid
from unittest.mock import AsyncMock

import pytest

from rivian.parallax.execute import ParallaxExecutionError, execute_command
from rivian.parallax.proto import command_pb2


class FakeAPI:
    def __init__(self, mode="success"):
        self.mode = mode
        self.order = []
        self.cleanup = AsyncMock()

    async def subscribe_for_parallax_command_state(self, vehicle, command_id, callback):
        self.order.append("subscribe")
        self.callback = callback
        if self.mode == "no_subscription":
            return None
        return self.cleanup

    def emit(self, command_id, status=1, progress=4, rvm="body.locks.lock"):
        message = command_pb2.CommandState(
            command_id=uuid.UUID(command_id).bytes,
            rvm=rvm,
            progress=progress,
        )
        message.data.response_status = status
        self.callback(
            {
                "payload": {
                    "data": {
                        "vehicleCommandStatePx": {
                            "payload": base64.b64encode(
                                message.SerializeToString()
                            ).decode()
                        }
                    }
                }
            }
        )

    async def send_parallax_command(self, *args, command_id, **kwargs):
        self.order.append("send")
        if self.mode == "exception":
            raise RuntimeError("SECRET response")
        if self.mode == "rejected":
            return None
        if self.mode == "wrong_id":
            self.emit(str(uuid.uuid4()))
        elif self.mode == "wrong_rvm":
            self.emit(command_id, rvm="body.locks.unlock")
        elif self.mode == "progress_only":
            self.emit(command_id, progress=3)
        elif self.mode == "failed":
            self.emit(command_id, status=2)
        elif self.mode == "success":
            self.emit(command_id)
            self.emit(command_id)  # duplicate terminal event must be harmless
        return command_id


async def run(api):
    return await execute_command(
        api,
        "synthetic-vehicle",
        "body.locks.lock",
        b"",
        identity_id="synthetic-id",
        vehicle_key="not-a-real-key",
        private_key="not-a-real-key",
        timeout=0.02,
    )


@pytest.mark.asyncio
async def test_success_subscribes_first_and_cleans_up():
    api = FakeAPI()
    assert uuid.UUID(await run(api))
    assert api.order == ["subscribe", "send"]
    api.cleanup.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mode",
    [
        "wrong_id",
        "wrong_rvm",
        "progress_only",
        "silent",
        "failed",
        "exception",
        "rejected",
    ],
)
async def test_no_false_success_or_retry(mode):
    api = FakeAPI(mode)
    with pytest.raises(ParallaxExecutionError) as exc:
        await run(api)
    assert "SECRET" not in str(exc.value)
    assert api.order == ["subscribe", "send"]
    api.cleanup.assert_awaited_once()


@pytest.mark.asyncio
async def test_subscription_required_before_send():
    api = FakeAPI("no_subscription")
    with pytest.raises(ParallaxExecutionError, match="not sent"):
        await run(api)
    assert api.order == ["subscribe"]


@pytest.mark.asyncio
async def test_cancellation_cleans_up_without_retry():
    api = FakeAPI("silent")
    task = asyncio.create_task(run(api))
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    api.cleanup.assert_awaited_once()
    assert api.order == ["subscribe", "send"]


@pytest.mark.asyncio
async def test_cleanup_failure_does_not_hide_success():
    api = FakeAPI()
    api.cleanup.side_effect = RuntimeError("cleanup")
    assert uuid.UUID(await run(api))


@pytest.mark.asyncio
async def test_failure_reports_status_without_raw_server_text():
    api = FakeAPI("failed")
    with pytest.raises(ParallaxExecutionError, match=r"status=failed, error_code=none"):
        await run(api)


@pytest.mark.asyncio
async def test_numeric_operation_error_excludes_server_message():
    api = FakeAPI("silent")

    async def send(*args, command_id, **kwargs):
        message = command_pb2.CommandState(
            command_id=uuid.UUID(command_id).bytes,
            rvm="body.locks.lock",
            progress=4,
        )
        message.data.response_status = 3
        message.data.error.code = 42
        message.data.error.message = "SECRET arbitrary server message"
        api.callback(
            {
                "payload": {
                    "data": {
                        "vehicleCommandStatePx": {
                            "payload": base64.b64encode(
                                message.SerializeToString()
                            ).decode()
                        }
                    }
                }
            }
        )
        return command_id

    api.send_parallax_command = send
    with pytest.raises(ParallaxExecutionError) as exc:
        await run(api)
    assert "status=invalid_request, error_code=42" in str(exc.value)
    assert "SECRET" not in str(exc.value)


@pytest.mark.asyncio
async def test_operation_error_reports_unknown_outcome_without_retry():
    api = FakeAPI("silent")

    async def send(*args, command_id, **kwargs):
        message = command_pb2.CommandState(
            command_id=uuid.UUID(command_id).bytes,
            rvm="body.locks.lock",
            progress=4,
        )
        message.operation_error.error = 3
        message.operation_error.message = "SECRET transport diagnostic"
        api.callback(
            {
                "payload": {
                    "data": {
                        "vehicleCommandStatePx": {
                            "payload": base64.b64encode(
                                message.SerializeToString()
                            ).decode()
                        }
                    }
                }
            }
        )
        return command_id

    api.send_parallax_command = AsyncMock(side_effect=send)
    with pytest.raises(ParallaxExecutionError) as exc:
        await run(api)
    assert "error_code=3" in str(exc.value)
    assert "outcome unknown; command may have taken effect" in str(exc.value)
    assert "SECRET" not in str(exc.value)
    api.send_parallax_command.assert_awaited_once()
    api.cleanup.assert_awaited_once()


@pytest.mark.asyncio
async def test_delayed_matching_success_after_progress_and_unrelated_events():
    api = FakeAPI("silent")
    sent = asyncio.Event()
    ids = []

    async def send(*args, command_id, **kwargs):
        ids.append(command_id)
        sent.set()
        return command_id

    api.send_parallax_command = AsyncMock(side_effect=send)
    task = asyncio.create_task(run(api))
    await sent.wait()
    api.emit(str(uuid.uuid4()))
    api.emit(ids[0], rvm="charging.energy.start_charging")
    api.emit(ids[0], progress=3)
    await asyncio.sleep(0)
    assert not task.done()
    api.emit(ids[0])
    assert await task == ids[0]
    api.send_parallax_command.assert_awaited_once()
    api.cleanup.assert_awaited_once()


@pytest.mark.asyncio
async def test_late_success_after_timeout_does_not_retry_or_raise_callback_error():
    api = FakeAPI("silent")
    ids = []

    async def send(*args, command_id, **kwargs):
        ids.append(command_id)
        return command_id

    api.send_parallax_command = AsyncMock(side_effect=send)
    with pytest.raises(ParallaxExecutionError, match="outcome unknown"):
        await run(api)
    # A callback already queued when unsubscribe completes must be harmless.
    api.emit(ids[0])
    api.emit(ids[0])
    api.send_parallax_command.assert_awaited_once()
    api.cleanup.assert_awaited_once()


@pytest.mark.asyncio
async def test_error_three_then_success_preserves_unknown_outcome():
    api = FakeAPI("silent")

    async def send(*args, command_id, **kwargs):
        message = command_pb2.CommandState(
            command_id=uuid.UUID(command_id).bytes,
            rvm="body.locks.lock",
            progress=4,
        )
        message.operation_error.error = 3
        message.operation_error.message = "SECRET simulated diagnostic"
        api.callback(
            {
                "payload": {
                    "data": {
                        "vehicleCommandStatePx": {
                            "payload": base64.b64encode(
                                message.SerializeToString()
                            ).decode()
                        }
                    }
                }
            }
        )
        api.emit(command_id)
        return command_id

    api.send_parallax_command = AsyncMock(side_effect=send)
    with pytest.raises(ParallaxExecutionError, match="outcome unknown") as exc:
        await run(api)
    assert "SECRET" not in str(exc.value)
    api.send_parallax_command.assert_awaited_once()
    api.cleanup.assert_awaited_once()


@pytest.mark.asyncio
async def test_subscription_timeout_never_submits_command():
    api = FakeAPI()

    async def subscribe(*args):
        await asyncio.Event().wait()

    api.subscribe_for_parallax_command_state = subscribe
    api.send_parallax_command = AsyncMock()
    with pytest.raises(
        ParallaxExecutionError, match="subscription timed out; command not sent"
    ):
        await run(api)
    api.send_parallax_command.assert_not_awaited()


@pytest.mark.asyncio
async def test_success_event_does_not_override_mismatched_cloud_acceptance():
    api = FakeAPI()

    async def send(*args, command_id, **kwargs):
        api.emit(command_id)
        return str(uuid.uuid4())

    api.send_parallax_command = AsyncMock(side_effect=send)
    with pytest.raises(ParallaxExecutionError, match="Cloud acceptance not confirmed"):
        await run(api)
    api.send_parallax_command.assert_awaited_once()
    api.cleanup.assert_awaited_once()


@pytest.mark.asyncio
async def test_unrelated_operation_error_does_not_fail_matching_command():
    api = FakeAPI()

    async def send(*args, command_id, **kwargs):
        message = command_pb2.CommandState(
            command_id=uuid.uuid4().bytes,
            rvm="body.locks.lock",
            progress=4,
        )
        message.operation_error.error = 3
        api.callback(
            {
                "payload": {
                    "data": {
                        "vehicleCommandStatePx": {
                            "payload": base64.b64encode(
                                message.SerializeToString()
                            ).decode()
                        }
                    }
                }
            }
        )
        api.emit(command_id)
        return command_id

    api.send_parallax_command = AsyncMock(side_effect=send)
    assert uuid.UUID(await run(api))
    api.send_parallax_command.assert_awaited_once()
    api.cleanup.assert_awaited_once()
