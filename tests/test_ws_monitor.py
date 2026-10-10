"""Tests for `rivian.ws_monitor`."""

# pylint: disable=protected-access
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import aiohttp
import pytest
from aiohttp import ClientWebSocketResponse, web

from rivian import ws_monitor
from rivian.ws_monitor import WebSocketMonitor


class FakeServer:
    """Web socket server that closes each connection with a queued reason."""

    def __init__(self) -> None:
        """Initialize the fake server."""
        self.close_reasons: list[str] = []
        self.connections = 0
        self.url = ""

    async def handler(self, request: web.Request) -> web.WebSocketResponse:
        """Handle a web socket connection."""
        ws = web.WebSocketResponse(protocols=("graphql-transport-ws",))
        await ws.prepare(request)
        self.connections += 1
        await ws.receive()  # connection_init
        if self.close_reasons:
            await ws.close(code=4000, message=self.close_reasons.pop(0).encode())
        else:
            await ws.send_json({"type": "connection_ack"})
            await ws.receive()
        return ws


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
    server: FakeServer, monitor: WebSocketMonitor
) -> None:
    """Test the monitor backs off and reconnects when rate limited."""
    server.close_reasons = ["Rate limited", "Rate limited"]
    delays: list[float] = []
    real_sleep = asyncio.sleep

    async def fake_sleep(delay: float) -> None:
        if delay >= ws_monitor.RATE_LIMIT_BACKOFF_MIN:
            delays.append(delay)
            delay = 0
        await real_sleep(delay)

    with patch.object(ws_monitor.asyncio, "sleep", fake_sleep):
        await monitor.new_connection(start_monitor=True)
        await wait_for(lambda: monitor.connection_ack.is_set())

    assert server.connections == 3
    assert monitor.connected
    assert monitor.monitor and not monitor.monitor.done()
    assert len(delays) == 2
    assert 30 <= delays[0] <= 60
    assert 60 <= delays[1] <= 90
