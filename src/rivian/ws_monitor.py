"""Websocket monitor."""

from __future__ import annotations

import asyncio
import inspect
import logging
import sys
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from json import loads
from random import uniform
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType

if sys.version_info >= (3, 11):
    import asyncio as async_timeout
else:
    import async_timeout

if TYPE_CHECKING:
    from .rivian import Rivian

_LOGGER = logging.getLogger(__name__)


async def cancel_task(*tasks: asyncio.Task | None) -> None:
    """Cancel task(s)."""
    for task in tasks:
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


class WebSocketMonitor:
    """Web socket monitor for a vehicle."""

    def __init__(
        self,
        account: Rivian,
        url: str,
        connection_init: Callable[[ClientWebSocketResponse], Awaitable[None]],
    ) -> None:
        """Initialize a web socket monitor."""
        self._account = account
        self._url = url
        self._connection_init = connection_init

        self._connection_ack: asyncio.Event = asyncio.Event()
        self._disconnect = False
        self._ws: ClientWebSocketResponse | None = None
        self._monitor_task: asyncio.Task | None = None
        self._receiver_task: asyncio.Task | None = None
        self._last_received: datetime | None = None
        self._subscriptions: dict[
            str, tuple[Callable[[dict[str, Any]], None], dict[str, Any]]
        ] = {}

    @property
    def connected(self) -> bool:
        """Return `True` if the web socket is connected."""
        if self._disconnect:
            return False
        return False if self._ws is None else not self._ws.closed

    @property
    def connection_ack(self) -> asyncio.Event:
        """Return `True` if the web socket connection is authenticated and acknowledged."""
        return self._connection_ack

    @property
    def websocket(self) -> ClientWebSocketResponse | None:
        """Return the web socket."""
        return self._ws

    @property
    def monitor(self) -> asyncio.Task | None:
        """Return the monitor task."""
        return self._monitor_task

    async def new_connection(self, start_monitor: bool = False) -> None:
        """Create a new connection and, optionally, start the monitor."""
        await cancel_task(self._receiver_task)
        self._disconnect = False
        # pylint: disable=protected-access
        assert self._account._session
        self._ws = await self._account._session.ws_connect(
            url=self._url, headers={"sec-websocket-protocol": "graphql-transport-ws"}
        )
        await self._connection_init(self._ws)
        self._receiver_task = asyncio.ensure_future(self._receiver())
        if start_monitor:
            await self.start_monitor()

    async def start_subscription(
        self, payload: dict[str, Any], callback: Callable[[dict[str, Any]], None]
    ) -> Callable[[], Awaitable[None]] | None:
        """Start a subscription."""
        if not self.connected:
            return None
        _id = str(uuid4())
        self._subscriptions[_id] = (callback, payload)
        await self._subscribe(_id, payload)

        async def unsubscribe() -> None:
            """Unsubscribe."""
            if _id in self._subscriptions:
                del self._subscriptions[_id]
                if self.connected:
                    assert self._ws
                    await self._ws.send_json({"id": _id, "type": "complete"})

        return unsubscribe

    async def _subscribe(self, _id: str, payload: dict[str, Any]) -> None:
        """Send a subscribe request."""
        assert self._ws
        await self._ws.send_json({"id": _id, "payload": payload, "type": "subscribe"})

    async def _resubscribe_all(self) -> None:
        """Resubscribe all subscriptions."""
        try:
            async with async_timeout.timeout(self._account.request_timeout):
                await self.connection_ack.wait()
        except asyncio.TimeoutError:
            _LOGGER.error("A timeout occurred while attempting to resubscribe")
            return
        for _id, (_, payload) in self._subscriptions.items():
            await self._subscribe(_id, payload)

    async def _receiver(self) -> None:
        """Receive a message from a web socket."""
        if not (websocket := self._ws):
            return
        while not websocket.closed:
            try:
                msg = await websocket.receive(timeout=60)
                if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                    self._log_message(msg)
                    if msg.extra == "Unauthenticated":
                        self._disconnect = True
                    break
                self._last_received = datetime.now(timezone.utc)
                if msg.type == WSMsgType.TEXT:
                    data = loads(msg.data)
                    if (data_type := data.get("type")) == "connection_ack":
                        self._connection_ack.set()
                    elif data_type == "next":
                        if (_id := data.get("id")) in self._subscriptions:
                            _fn = self._subscriptions[_id][0]
                            if inspect.iscoroutinefunction(_fn):
                                await _fn(data)
                            else:
                                _fn(data)
                    else:
                        self._log_message(msg)
                elif msg.type == WSMsgType.ERROR:
                    self._log_message(msg, True)
                    continue
            except asyncio.TimeoutError:
                await self._resubscribe_all()
        self._connection_ack.clear()
        self._log_message("web socket stopped")

    async def _monitor(self) -> None:
        """Monitor a web socket connection."""
        attempt = 0
        while not self._disconnect:
            while self.connected:
                if self._receiver_task and self._receiver_task.done():
                    # Need to restart the receiver
                    self._receiver_task = asyncio.ensure_future(self._receiver())
                await asyncio.sleep(1)
            if not self._disconnect:
                try:
                    await self.new_connection()
                except Exception as ex:  # pylint: disable=broad-except
                    self._log_message(ex, True)
                if not self._ws or self._ws.closed:
                    await asyncio.sleep(min(1 * 2**attempt + uniform(0, 1), 300))
                    attempt += 1
                    continue
                attempt = 0
                self._log_message("web socket connection reopened")
                await self._resubscribe_all()

    async def start_monitor(self) -> None:
        """Start or restart the monitor task."""
        if self._monitor_task is None or self._monitor_task.done():
            self._monitor_task = asyncio.ensure_future(self._monitor())

    async def stop_monitor(self) -> None:
        """Stop the monitor task."""
        await cancel_task(self._monitor_task)

    async def close(self) -> None:
        """Close the web socket."""
        self._disconnect = True
        if self._ws:
            await self._ws.close()
        await cancel_task(self._monitor_task, self._receiver_task)

    def _log_message(
        self, message: str | Exception | WSMessage, is_error: bool = False
    ) -> None:
        """Log a message."""
        log_method = _LOGGER.error if is_error else _LOGGER.debug
        log_method(message)
