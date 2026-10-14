"""Tests for `rivian.ws_monitor`."""

# pylint: disable=protected-access
from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator, Iterator
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import aiohttp
import pytest
from aiohttp import ClientWebSocketResponse, WSMsgType, web

from rivian import Rivian, ws_monitor
from rivian.ws_monitor import WebSocketMonitor


class FakeServer:
    """Web socket server that acks, ignores, pings or closes each connection."""

    def __init__(self) -> None:
        """Initialize the fake server."""
        self.close_reasons: list[str] = []
        self.silent_connections = 0
        self.ping_connections = 0
        self.ping_once_connections = 0
        self.connections = 0
        self.next_on_subscribe = False
        self.url = ""

    async def handler(self, request: web.Request) -> web.WebSocketResponse:
        """Handle a web socket connection."""
        ws = web.WebSocketResponse(protocols=("graphql-transport-ws",))
        await ws.prepare(request)
        self.connections += 1
        await ws.receive()  # connection_init
        if self.silent_connections:
            # Never send connection_ack; wait for the client to close
            self.silent_connections -= 1
            await ws.receive()
        elif self.ping_connections:
            # Never send connection_ack; send pings until the client closes
            self.ping_connections -= 1
            while not ws.closed:
                try:
                    msg = await ws.receive(timeout=0.2)
                except TimeoutError:
                    await ws.send_json({"type": "ping"})
                    continue
                if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                    break
        elif self.ping_once_connections:
            # Never send connection_ack; send one ping, then wait for the client to close
            self.ping_once_connections -= 1
            await ws.send_json({"type": "ping"})
            await ws.receive()
        elif self.close_reasons:
            await ws.close(code=4000, message=self.close_reasons.pop(0).encode())
        else:
            await ws.send_json({"type": "connection_ack"})
            # Take subscribe requests until the client closes
            async for msg in ws:
                data = msg.json()
                if self.next_on_subscribe and data.get("type") == "subscribe":
                    await ws.send_json({"id": data["id"], "type": "next"})
        return ws


# The monitor sleeps for what's left of a backoff, so allow for time passing
# between recording one and sleeping
BACKOFF_SLACK = 5


class BackoffSleeps:
    """Backoff delays requested by the monitor."""

    def __init__(self) -> None:
        """Initialize."""
        self.delays: list[float] = []
        self.skipped = 0.0  # total of the delays skipped, added to the monitor's clock
        self.hold = False
        self.release = asyncio.Event()


@pytest.fixture
async def server() -> AsyncIterator[FakeServer]:
    """Run a fake web socket server."""
    fake = FakeServer()
    app = web.Application()
    app.router.add_get("/", fake.handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]
    fake.url = f"http://127.0.0.1:{port}/"
    yield fake
    await runner.cleanup()


@pytest.fixture
async def monitor(server: FakeServer) -> AsyncIterator[WebSocketMonitor]:
    """Create a web socket monitor connected to the fake server."""

    async def connection_init(ws: ClientWebSocketResponse[bool]) -> None:
        await ws.send_json({"type": "connection_init"})

    async with aiohttp.ClientSession() as session:
        account: Any = SimpleNamespace(_session=session, request_timeout=1)
        mon = WebSocketMonitor(account, server.url, connection_init)
        yield mon
        await mon.close()


@pytest.fixture
async def rivian(monitor: WebSocketMonitor) -> AsyncIterator[Rivian]:
    """Create a client that uses the monitor."""
    async with aiohttp.ClientSession() as session:
        client = Rivian(request_timeout=1, session=session)
        client._ws_monitor = monitor
        yield client


@pytest.fixture
def backoff() -> Iterator[BackoffSleeps]:
    """Record backoff delays instead of sleeping; wait for `release` if `hold`.

    The monitor's clock moves forward by each skipped delay, so the backoff passes.
    """
    sleeps = BackoffSleeps()
    real_sleep = asyncio.sleep

    async def fake_sleep(delay: float) -> None:
        # Anything longer than the monitor's 1 second poll is a backoff
        if delay > 1:
            sleeps.delays.append(delay)
            if sleeps.hold:
                await sleeps.release.wait()
            sleeps.skipped += delay
            delay = 0
        await real_sleep(delay)

    clock = SimpleNamespace(monotonic=lambda: time.monotonic() + sleeps.skipped)
    with (
        patch.object(ws_monitor.asyncio, "sleep", fake_sleep),
        patch.object(ws_monitor, "time", clock),
    ):
        yield sleeps


def add_subscription(monitor: WebSocketMonitor) -> None:
    """Give the monitor a subscription to resume, so it keeps reconnecting."""
    monitor._subscriptions["sub"] = (lambda _: None, {"query": "subscription"})


async def wait_for(condition: Any, timeout: float = 5) -> None:
    """Wait for a condition to be true."""
    async with asyncio.timeout(timeout):
        while not condition():
            await asyncio.sleep(0.05)


async def test_unauthenticated_stops_monitor(
    server: FakeServer, monitor: WebSocketMonitor
) -> None:
    """Test the monitor stops reconnecting when unauthenticated."""
    server.close_reasons = ["Unauthenticated"]
    await monitor.new_connection(start_monitor=True)
    assert monitor.monitor
    await wait_for(monitor.monitor.done)
    assert server.connections == 1
    assert not monitor.connected


async def test_rate_limited_backs_off_and_reconnects(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test the monitor backs off and reconnects when rate limited."""
    server.close_reasons = ["Rate limited", "Rate limited"]
    add_subscription(monitor)
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: monitor.connection_ack.is_set())

    assert server.connections == 3
    assert monitor.connected
    assert monitor.monitor and not monitor.monitor.done()
    assert len(backoff.delays) == 2
    assert 30 - BACKOFF_SLACK <= backoff.delays[0] <= 60
    assert 60 - BACKOFF_SLACK <= backoff.delays[1] <= 90


async def test_unacknowledged_connection_backs_off_and_reconnects(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test the monitor backs off when a connection is never acknowledged."""
    server.silent_connections = 2
    add_subscription(monitor)
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: monitor.connection_ack.is_set())

    assert server.connections == 3
    assert len(backoff.delays) == 2
    assert 30 - BACKOFF_SLACK <= backoff.delays[0] <= 60
    assert 60 - BACKOFF_SLACK <= backoff.delays[1] <= 90


async def test_messages_before_ack_do_not_extend_ack_timeout(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test pings without connection_ack still lead to a backoff."""
    server.ping_connections = 1
    add_subscription(monitor)
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: monitor.connection_ack.is_set())

    assert server.connections == 2
    assert len(backoff.delays) == 1


async def test_ack_deadline_passed_while_handling_a_message(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test the ack deadline still applies once it passes between two receives."""
    server.ping_once_connections = 1
    monitor._account.request_timeout = 0.2
    log_message = monitor._log_message

    def slow_log_message(message: Any, is_error: bool = False) -> None:
        # Handling the ping takes until after the ack deadline
        if getattr(message, "type", None) == WSMsgType.TEXT:
            time.sleep(0.3)
        log_message(message, is_error)

    with patch.object(monitor, "_log_message", slow_log_message):
        add_subscription(monitor)
        await monitor.new_connection(start_monitor=True)
        await wait_for(lambda: monitor.connection_ack.is_set())

    assert server.connections == 2
    assert len(backoff.delays) == 1


async def test_new_connection_is_not_acknowledged_yet(
    server: FakeServer, monitor: WebSocketMonitor
) -> None:
    """Test a new connection does not inherit the previous connection's ack."""
    await monitor.new_connection()
    await wait_for(lambda: monitor.connection_ack.is_set())

    server.silent_connections = 1
    await monitor.new_connection()

    assert not monitor.connection_ack.is_set()


async def test_subscribe_does_not_connect_during_backoff(
    server: FakeServer,
    monitor: WebSocketMonitor,
    rivian: Rivian,
    backoff: BackoffSleeps,
) -> None:
    """Test a new subscription does not open a connection while backing off."""
    server.close_reasons = ["Rate limited"]
    backoff.hold = True
    add_subscription(monitor)
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: len(backoff.delays) == 1)

    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert server.connections == 1


async def test_subscribe_does_not_connect_before_backoff_starts(
    server: FakeServer, monitor: WebSocketMonitor, rivian: Rivian
) -> None:
    """Test a subscription does not connect when a backoff is pending."""
    monitor._start_backoff(ws_monitor.BACKOFF_RATE_LIMITED)

    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert server.connections == 0


async def test_monitor_stops_with_nothing_subscribed(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test a monitor with no subscriptions stops instead of reconnecting."""
    server.close_reasons = ["Rate limited"]
    await monitor.new_connection(start_monitor=True)
    assert monitor.monitor
    await wait_for(monitor.monitor.done)

    assert server.connections == 1
    assert backoff.delays == []  # nothing waited on
    assert monitor.backing_off  # but the next connection still waits


async def test_backoff_is_shared_by_key(server: FakeServer) -> None:
    """Test a new monitor waits out the backoff of another with the same key."""

    async def connection_init(ws: ClientWebSocketResponse[bool]) -> None:
        await ws.send_json({"type": "connection_init"})

    server.close_reasons = ["Rate limited"]
    async with aiohttp.ClientSession() as session:
        account: Any = SimpleNamespace(_session=session, request_timeout=1)
        first = WebSocketMonitor(account, server.url, connection_init, "session")
        await first.new_connection(start_monitor=True)
        assert first.monitor
        await wait_for(first.monitor.done)
        await first.close()

        second = WebSocketMonitor(account, server.url, connection_init, "session")
        other = WebSocketMonitor(account, server.url, connection_init, "other")
        try:
            assert second.backing_off
            assert (
                second.backoff_remaining
                >= ws_monitor.RATE_LIMIT_BACKOFF_MIN - BACKOFF_SLACK
            )
            assert not other.backing_off
        finally:
            WebSocketMonitor._shared_backoffs.clear()


async def test_failed_subscribe_logs_reason_and_closes(
    server: FakeServer,
    monitor: WebSocketMonitor,
    rivian: Rivian,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test a failed subscription logs why and leaves nothing reconnecting."""
    server.silent_connections = 1

    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert (
        "Unable to subscribe to id vehicle updates: the web socket connection was not "
        "acknowledged" in caplog.text
    )
    assert monitor.monitor and monitor.monitor.done()
    assert not monitor.connected


async def test_rate_limited_subscribe_fails_fast(
    server: FakeServer,
    monitor: WebSocketMonitor,
    rivian: Rivian,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test a rate limit before the ack fails the subscribe without waiting it out."""
    server.close_reasons = ["Rate limited"]
    monitor._account.request_timeout = 10

    start = time.monotonic()
    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert time.monotonic() - start < 2
    assert (
        "Unable to subscribe to id vehicle updates: the web socket connection was rate limited"
        in caplog.text
    )
    assert monitor.backing_off
    assert (
        rivian.ws_backoff_remaining >= ws_monitor.RATE_LIMIT_BACKOFF_MIN - BACKOFF_SLACK
    )
    assert rivian.ws_rate_limited


async def test_backoff_survives_close_after_failed_subscribe(
    server: FakeServer, monitor: WebSocketMonitor, rivian: Rivian
) -> None:
    """Test closing after a failed subscribe keeps its backoff for the next one."""
    server.silent_connections = 1

    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert rivian.ws_backoff_remaining > 0
    assert not rivian.ws_rate_limited  # not acknowledged, rather than rate limited

    # The next subscribe doesn't connect until the backoff has passed
    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert server.connections == 1

    monitor._backoff_state.retry_at = 0
    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None)
    assert server.connections == 2
    assert rivian.ws_backoff_remaining == 0


async def test_unsubscribing_last_subscription_closes(
    server: FakeServer, monitor: WebSocketMonitor, rivian: Rivian
) -> None:
    """Test the connection closes with its last subscription, and reopens after."""
    first = await rivian.subscribe_for_vehicle_updates("id", lambda _: None)
    second = await rivian.subscribe_for_parallax_messages("id", lambda _: None)
    assert first and second

    await first()
    assert monitor.connected
    await second()
    assert not monitor.connected
    assert monitor.monitor and monitor.monitor.done()

    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None)
    assert monitor.connected
    assert server.connections == 2


async def test_failing_callback_keeps_connection(
    server: FakeServer,
    monitor: WebSocketMonitor,
    rivian: Rivian,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test a callback that raises doesn't lose the ack or back off."""
    server.next_on_subscribe = True
    calls = 0

    def callback(_: dict[str, Any]) -> None:
        nonlocal calls
        calls += 1
        raise ValueError("callback failed")

    assert await rivian.subscribe_for_vehicle_updates("id", callback)
    await wait_for(lambda: calls == 1)
    await asyncio.sleep(1.5)  # past the 1 second ack deadline

    assert "Error in a subscription callback" in caplog.text
    assert monitor.connection_ack.is_set()
    assert monitor.connected
    assert not monitor.backing_off
    assert server.connections == 1


async def test_backoff_does_not_block_an_open_connection(
    server: FakeServer, monitor: WebSocketMonitor, rivian: Rivian
) -> None:
    """Test a shared backoff only holds off new connections."""
    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None)
    # As if another client on the same session was rate limited
    monitor._backoff_state.retry_at = time.monotonic() + 60

    assert await rivian.subscribe_for_parallax_messages("id", lambda _: None)
    assert server.connections == 1


async def test_backoff_pushed_back_while_waiting(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test the monitor waits again if the backoff is pushed back meanwhile."""
    server.close_reasons = ["Rate limited"]
    backoff.hold = True
    add_subscription(monitor)
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: len(backoff.delays) == 1)

    # As if another client on the same session was rate limited meanwhile
    monitor._backoff_state.retry_at = ws_monitor.time.monotonic() + 100
    backoff.release.set()
    await wait_for(lambda: monitor.connection_ack.is_set())

    assert len(backoff.delays) == 2
    # The rest of the pushed-back backoff, after the first delay has passed
    assert backoff.delays[1] == pytest.approx(
        100 - backoff.delays[0], abs=BACKOFF_SLACK
    )
    assert server.connections == 2
