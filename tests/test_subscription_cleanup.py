"""Interrupted registration must not leave subscriptions to reconnect later."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from rivian.parallax.execute import ParallaxExecutionError, execute_command
from rivian.ws_monitor import WebSocketMonitor


def make_monitor() -> WebSocketMonitor:
    """Use the real monitor with an in-memory transport, without opening sockets."""
    account: Any = SimpleNamespace(request_timeout=1)
    monitor = WebSocketMonitor(account, "unused", AsyncMock())
    monitor._ws = SimpleNamespace(  # type: ignore[assignment]
        closed=False, send_json=AsyncMock(), close=AsyncMock()
    )
    return monitor


@pytest.mark.parametrize("keep_existing", [False, True])
@pytest.mark.parametrize("failure", ["cancel", "send_error", "timeout"])
async def test_interrupted_registration_cleans_only_its_subscription(
    keep_existing: bool, failure: str
) -> None:
    """A send failure, cancellation or deadline preserves unrelated subscriptions."""
    monitor = make_monitor()
    assert monitor.websocket
    transport: Any = monitor.websocket
    existing = (lambda _: None, {"existing": True})
    if keep_existing:
        monitor._subscriptions["existing"] = existing
    started = asyncio.Event()
    send_error = RuntimeError("send failed")

    async def send(data: dict[str, Any]) -> None:
        if data["type"] == "subscribe":
            started.set()
            if failure == "send_error":
                raise send_error
            await asyncio.Event().wait()

    transport.send_json.side_effect = send

    async def subscribe() -> None:
        if failure == "timeout":
            async with asyncio.timeout(0.01):
                await monitor.start_subscription({}, lambda _: None)
        else:
            await monitor.start_subscription({}, lambda _: None)

    task = asyncio.create_task(subscribe())
    await started.wait()
    if failure == "cancel":
        task.cancel()
    expected = {
        "cancel": asyncio.CancelledError,
        "send_error": RuntimeError,
        "timeout": TimeoutError,
    }[failure]
    with pytest.raises(expected) as caught:
        await task
    if failure == "send_error":
        assert caught.value is send_error
    assert monitor._subscriptions == ({"existing": existing} if keep_existing else {})
    if keep_existing:
        transport.close.assert_not_awaited()
        sent = transport.send_json.call_args_list
        assert sent[-1].args[0]["type"] == "complete"
        assert sent[-1].args[0]["id"] == sent[0].args[0]["id"]
    else:
        transport.close.assert_awaited_once()


async def test_execution_timeout_cleans_real_monitor_registration() -> None:
    """Exercise the helper deadline with the actual monitor, not a fake subscriber."""
    monitor = make_monitor()
    transport: Any = monitor.websocket

    async def send(_: dict[str, Any]) -> None:
        await asyncio.Event().wait()

    transport.send_json.side_effect = send

    async def subscribe(vehicle: str, command_id: str, callback: Any) -> Any:
        return await monitor.start_subscription({"commandId": command_id}, callback)

    api = SimpleNamespace(
        subscribe_for_parallax_command_state=subscribe,
        send_parallax_command=AsyncMock(),
    )
    with pytest.raises(ParallaxExecutionError, match="command not sent"):
        await execute_command(
            api,
            "vehicle",
            "body.locks.lock",
            b"",
            identity_id="identity",
            vehicle_key="synthetic",
            private_key="synthetic",
            timeout=0.01,
        )
    assert not monitor.has_subscriptions
    transport.close.assert_awaited_once()
    api.send_parallax_command.assert_not_awaited()


@pytest.mark.parametrize("keep_existing", [False, True])
async def test_cleanup_timeout_preserves_original_error(keep_existing: bool) -> None:
    """A stuck close or completion send cannot hide the registration error."""
    monitor = make_monitor()
    transport: Any = monitor.websocket
    if keep_existing:
        monitor._subscriptions["existing"] = (lambda _: None, {})
    original = RuntimeError("send failed")

    async def stuck(*_: Any) -> None:
        await asyncio.Event().wait()

    async def send(data: dict[str, Any]) -> None:
        if data["type"] == "subscribe":
            raise original
        await stuck()

    transport.send_json.side_effect = send
    transport.close.side_effect = stuck
    real_timeout = asyncio.timeout
    with (
        patch(
            "rivian.ws_monitor.asyncio.timeout", return_value=real_timeout(0.01)
        ) as timeout,
        pytest.raises(RuntimeError) as caught,
    ):
        await monitor.start_subscription({}, lambda _: None)
    timeout.assert_called_once_with(5)
    assert caught.value is original
    assert set(monitor._subscriptions) == ({"existing"} if keep_existing else set())


@pytest.mark.parametrize("phase", ["connect", "ack"])
@pytest.mark.parametrize("keep_existing", [False, True])
async def test_client_cancellation_before_registration(
    phase: str, keep_existing: bool
) -> None:
    """An interrupted connection/ack closes only an otherwise unused monitor."""
    from rivian import Rivian

    monitor = make_monitor()
    transport: Any = monitor.websocket
    monitor._closed.clear()
    if keep_existing:
        monitor._subscriptions["existing"] = (lambda _: None, {})
    client = Rivian(request_timeout=60)
    client._ws_monitor = monitor
    started = asyncio.Event()
    original_wait = monitor.wait_for_ack

    async def connect() -> WebSocketMonitor:
        if phase == "connect":
            started.set()
            await asyncio.Event().wait()
        return monitor

    async def wait() -> bool:
        started.set()
        return await original_wait()

    with (
        patch.object(client, "_ws_connect", side_effect=connect),
        patch.object(monitor, "wait_for_ack", side_effect=wait),
    ):
        task = asyncio.create_task(
            client._start_subscription({}, lambda _: None, "test")
        )
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    assert set(monitor._subscriptions) == ({"existing"} if keep_existing else set())
    if keep_existing:
        transport.close.assert_not_awaited()
        assert monitor.connected
    else:
        transport.close.assert_awaited_once()
        assert not monitor.connected


async def test_client_cancellation_cleanup_is_bounded() -> None:
    """A stuck close cannot indefinitely delay the original cancellation."""
    from rivian import Rivian

    monitor = make_monitor()
    transport: Any = monitor.websocket
    client = Rivian(request_timeout=60)
    client._ws_monitor = monitor
    started = asyncio.Event()

    async def connect() -> WebSocketMonitor:
        started.set()
        await asyncio.Event().wait()
        return monitor

    async def stuck() -> None:
        await asyncio.Event().wait()

    transport.close.side_effect = stuck
    real_timeout = asyncio.timeout
    with patch.object(client, "_ws_connect", side_effect=connect):
        task = asyncio.create_task(
            client._start_subscription({}, lambda _: None, "test")
        )
        await started.wait()
        with patch(
            "rivian.rivian.asyncio.timeout", return_value=real_timeout(0.01)
        ) as timeout:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        timeout.assert_called_once_with(5)
    assert not monitor.has_subscriptions
    transport.close.assert_awaited_once()
