"""Tests for `rivian.ws_monitor`."""

# pylint: disable=protected-access
from __future__ import annotations

import asyncio
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
        self.connections = 0
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
                except asyncio.TimeoutError:
                    await ws.send_json({"type": "ping"})
                    continue
                if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                    break
        elif self.close_reasons:
            await ws.close(code=4000, message=self.close_reasons.pop(0).encode())
        else:
            await ws.send_json({"type": "connection_ack"})
            await ws.receive()
        return ws


class BackoffSleeps:
    """Backoff delays requested by the monitor."""

    def __init__(self) -> None:
        """Initialize."""
        self.delays: list[float] = []
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
    """Record backoff delays instead of sleeping; wait for `release` if `hold`."""
    sleeps = BackoffSleeps()
    real_sleep = asyncio.sleep

    async def fake_sleep(delay: float) -> None:
        if delay >= ws_monitor.RATE_LIMIT_BACKOFF_MIN:
            sleeps.delays.append(delay)
            if sleeps.hold:
                await sleeps.release.wait()
            delay = 0
        await real_sleep(delay)

    with patch.object(ws_monitor.asyncio, "sleep", fake_sleep):
        yield sleeps


async def wait_for(condition: Any, timeout: float = 5) -> None:
    """Wait for a condition to be true."""
    async with ws_monitor.async_timeout.timeout(timeout):
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
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: monitor.connection_ack.is_set())

    assert server.connections == 3
    assert monitor.connected
    assert monitor.monitor and not monitor.monitor.done()
    assert len(backoff.delays) == 2
    assert 30 <= backoff.delays[0] <= 60
    assert 60 <= backoff.delays[1] <= 90


async def test_unacknowledged_connection_backs_off_and_reconnects(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test the monitor backs off when a connection is never acknowledged."""
    server.silent_connections = 2
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: monitor.connection_ack.is_set())

    assert server.connections == 3
    assert len(backoff.delays) == 2
    assert 30 <= backoff.delays[0] <= 60
    assert 60 <= backoff.delays[1] <= 90


async def test_messages_before_ack_do_not_extend_ack_timeout(
    server: FakeServer, monitor: WebSocketMonitor, backoff: BackoffSleeps
) -> None:
    """Test pings without connection_ack still lead to a backoff."""
    server.ping_connections = 1
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
    await monitor.new_connection(start_monitor=True)
    await wait_for(lambda: len(backoff.delays) == 1)

    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert server.connections == 1


async def test_subscribe_does_not_connect_before_backoff_starts(
    server: FakeServer, monitor: WebSocketMonitor, rivian: Rivian
) -> None:
    """Test a subscription does not connect when a backoff is pending."""
    monitor._backoff_reason = "was rate limited"

    assert await rivian.subscribe_for_vehicle_updates("id", lambda _: None) is None
    assert server.connections == 0
