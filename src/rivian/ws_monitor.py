"""Websocket monitor."""

from __future__ import annotations

import asyncio
import inspect
import logging
import time
from collections.abc import Awaitable, Callable, Hashable
from dataclasses import dataclass
from datetime import UTC, datetime
from json import loads
from random import uniform
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import uuid4

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType
from aiohttp.http_websocket import WSMessageTextBytes

if TYPE_CHECKING:
    from .rivian import Rivian

_LOGGER = logging.getLogger(__name__)

RATE_LIMITED = "Rate limited"
UNAUTHENTICATED = "Unauthenticated"
RATE_LIMIT_BACKOFF_MIN = 30
RATE_LIMIT_BACKOFF_MAX = 900

# Backoff reasons, completing "the web socket connection ..."
BACKOFF_RATE_LIMITED = "was rate limited"
BACKOFF_NOT_ACKNOWLEDGED = "was not acknowledged"


async def cancel_task(*tasks: asyncio.Task | None) -> None:
    """Cancel task(s), other than the one running this."""
    current = asyncio.current_task()
    for task in tasks:
        if task is not None and task is not current and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


@dataclass
class _Backoff:
    """Backoff state: consecutive failed connections and when to retry."""

    attempt: int = 0
    retry_at: float = 0  # time.monotonic()
    rate_limited: bool = False  # whether the backoff until retry_at is a rate limit


class WebSocketMonitor:
    """Web socket monitor for a vehicle."""

    # Backoff state by key, shared so a new monitor for the same session doesn't
    # connect while another is waiting out a rate limit
    _shared_backoffs: ClassVar[dict[Hashable, _Backoff]] = {}

    def __init__(
        self,
        account: Rivian,
        url: str,
        connection_init: Callable[[ClientWebSocketResponse[bool]], Awaitable[None]],
        backoff_key: Hashable | None = None,
    ) -> None:
        """Initialize a web socket monitor.

        Monitors with the same `backoff_key` (e.g. the user session) share their
        backoff state; without one, the state is the monitor's own.
        """
        self._account = account
        self._url = url
        self._connection_init = connection_init

        self._connection_ack: asyncio.Event = asyncio.Event()
        # Set while there's no open connection
        self._closed: asyncio.Event = asyncio.Event()
        self._closed.set()
        self._disconnect = False
        # Why the current connection is backing off, at most once per connection
        self._backoff_reason: str | None = None
        # The server's reason for closing the current connection, if it gave one
        self._close_message: str | None = None
        self._backoff_state = (
            _Backoff()
            if backoff_key is None
            else self._shared_backoffs.setdefault(backoff_key, _Backoff())
        )
        self._ws: ClientWebSocketResponse[bool] | None = None
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
    def websocket(self) -> ClientWebSocketResponse[bool] | None:
        """Return the web socket."""
        return self._ws

    @property
    def monitor(self) -> asyncio.Task | None:
        """Return the monitor task."""
        return self._monitor_task

    @property
    def backing_off(self) -> bool:
        """Return `True` while waiting to reconnect after a failed connection."""
        return self.backoff_remaining > 0

    @property
    def backoff_reason(self) -> str | None:
        """Return why the latest connection is backing off, if it is."""
        return self._backoff_reason

    @property
    def close_message(self) -> str | None:
        """Return the server's reason for closing the latest connection, if any."""
        return self._close_message

    @property
    def rate_limited(self) -> bool:
        """Return `True` while backing off after a rate limit.

        Shared like the backoff, so a new monitor for the same session sees it too.
        """
        return self._backoff_state.rate_limited and self.backoff_remaining > 0

    @property
    def unauthenticated(self) -> bool:
        """Return `True` if the server closed the latest connection as unauthenticated."""
        return self._close_message == UNAUTHENTICATED

    @property
    def backoff_remaining(self) -> float:
        """Return the seconds left before reconnecting is allowed."""
        return max(self._backoff_state.retry_at - time.monotonic(), 0)

    @property
    def has_subscriptions(self) -> bool:
        """Return `True` if there are subscriptions to resume on reconnect."""
        return bool(self._subscriptions)

    async def new_connection(self, start_monitor: bool = False) -> None:
        """Create a new connection and, optionally, start the monitor."""
        await cancel_task(self._receiver_task)
        self._disconnect = False
        self._backoff_reason = None
        self._close_message = None
        self._connection_ack.clear()
        # pylint: disable=protected-access
        assert self._account._session
        self._ws = await self._account._session.ws_connect(
            url=self._url, headers={"sec-websocket-protocol": "graphql-transport-ws"}
        )
        await self._connection_init(self._ws)
        self._closed.clear()
        self._receiver_task = asyncio.ensure_future(self._receiver())
        if start_monitor:
            await self.start_monitor()

    async def wait_for_ack(self) -> bool:
        """Wait for the connection to be acknowledged or to close.

        Returns whether it was acknowledged. A connection that isn't acknowledged
        within the request timeout is closed and backed off.
        """
        if not self._connection_ack.is_set():
            waits = [
                asyncio.ensure_future(self._connection_ack.wait()),
                asyncio.ensure_future(self._closed.wait()),
            ]
            try:
                done, _ = await asyncio.wait(
                    waits,
                    timeout=self._account.request_timeout,
                    return_when=asyncio.FIRST_COMPLETED,
                )
            finally:
                await cancel_task(*waits)
            if not done:
                self._start_backoff(BACKOFF_NOT_ACKNOWLEDGED)
                if self._ws:
                    await self._ws.close()
        return self._connection_ack.is_set()

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
                if not self._subscriptions:
                    # Don't keep a connection open with nothing on it; the next
                    # subscription reconnects
                    await self.close()

        return unsubscribe

    async def _subscribe(self, _id: str, payload: dict[str, Any]) -> None:
        """Send a subscribe request."""
        assert self._ws
        await self._ws.send_json({"id": _id, "payload": payload, "type": "subscribe"})

    async def _resubscribe_all(self) -> None:
        """Resubscribe all subscriptions."""
        try:
            async with asyncio.timeout(self._account.request_timeout):
                await self.connection_ack.wait()
        except TimeoutError:
            _LOGGER.error("A timeout occurred while attempting to resubscribe")
            return
        for _id, (_, payload) in self._subscriptions.items():
            await self._subscribe(_id, payload)

    async def _receiver(self) -> None:
        """Receive a message from a web socket."""
        if not (websocket := self._ws):
            return
        try:
            await self._receive(websocket)
        finally:
            # A receiver restarted on an open connection keeps its ack
            if websocket.closed:
                self._connection_ack.clear()
                self._closed.set()
        self._log_message("web socket stopped")

    async def _receive(self, websocket: ClientWebSocketResponse[bool]) -> None:
        """Handle messages until the web socket closes."""
        loop = asyncio.get_running_loop()
        ack_deadline = loop.time() + self._account.request_timeout
        while not websocket.closed:
            acknowledged = self._connection_ack.is_set()
            try:
                if acknowledged:
                    timeout = 60.0
                # aiohttp treats a timeout of 0 as no timeout, so time out here instead
                elif (timeout := ack_deadline - loop.time()) <= 0:
                    raise TimeoutError
                msg = await websocket.receive(timeout=timeout)
                if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                    self._log_message(msg)
                    self._close_message = msg.extra or None
                    if msg.extra == UNAUTHENTICATED:
                        self._disconnect = True
                    elif msg.extra == RATE_LIMITED:
                        self._start_backoff(BACKOFF_RATE_LIMITED)
                    break
                self._last_received = datetime.now(UTC)
                if msg.type == WSMsgType.TEXT:
                    data = loads(msg.data)
                    if (data_type := data.get("type")) == "connection_ack":
                        self._connection_ack.set()
                    elif data_type == "next":
                        self._reset_backoff()
                        if (_id := data.get("id")) in self._subscriptions:
                            _fn = self._subscriptions[_id][0]
                            # A failing callback shouldn't take the connection down
                            try:
                                if inspect.iscoroutinefunction(_fn):
                                    await _fn(data)
                                else:
                                    _fn(data)
                            except Exception:  # pylint: disable=broad-except
                                _LOGGER.exception("Error in a subscription callback")
                    else:
                        self._log_message(msg)
                elif msg.type == WSMsgType.ERROR:
                    self._log_message(msg, True)
                    continue
            except TimeoutError:
                if not acknowledged:
                    self._start_backoff(BACKOFF_NOT_ACKNOWLEDGED)
                    await websocket.close()
                    break
                # The connection has stayed open, so any rate limit has passed
                self._reset_backoff()
                await self._resubscribe_all()

    async def _monitor(self) -> None:
        """Monitor a web socket connection."""
        attempt = 0
        while not self._disconnect:
            while self.connected:
                if self._receiver_task and self._receiver_task.done():
                    # Need to restart the receiver
                    self._receiver_task = asyncio.ensure_future(self._receiver())
                await asyncio.sleep(1)
            if not self._subscriptions:
                # Nothing to resume, so stop rather than keep reconnecting; the
                # next subscription reconnects once any backoff has passed
                self._log_message("web socket monitor stopped, nothing subscribed")
                break
            while delay := self.backoff_remaining:
                # Re-check after waiting, as another monitor for the same session
                # may have pushed the retry back
                await asyncio.sleep(delay)
            if self._disconnect or self.connected:
                continue
            if not self._disconnect:
                try:
                    await self.new_connection()
                except Exception as ex:  # pylint: disable=broad-except # noqa: BLE001
                    self._log_message(ex, True)
                if not self._ws or self._ws.closed:
                    await asyncio.sleep(min(1 * 2**attempt + uniform(0, 1), 300))
                    attempt += 1
                    continue
                attempt = 0
                self._log_message("web socket connection reopened")
                await self._resubscribe_all()

    def _start_backoff(self, reason: str) -> None:
        """Hold off reconnecting after a rate limit or a missing connection_ack.

        The retry time is recorded right away, so closing the monitor can't lose
        it; a connection backs off at most once.
        """
        if self._backoff_reason:
            return
        self._backoff_reason = reason
        state = self._backoff_state
        delay = min(
            RATE_LIMIT_BACKOFF_MIN * 2**state.attempt
            + uniform(0, RATE_LIMIT_BACKOFF_MIN),
            RATE_LIMIT_BACKOFF_MAX,
        )
        state.attempt += 1
        state.retry_at = time.monotonic() + delay
        state.rate_limited = reason == BACKOFF_RATE_LIMITED
        _LOGGER.warning(
            "Web socket connection %s, reconnecting in %.0f seconds", reason, delay
        )

    def _reset_backoff(self) -> None:
        """Start the next backoff over, now that the connection is healthy."""
        self._backoff_state.attempt = 0

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
        self,
        message: str | Exception | WSMessage | WSMessageTextBytes,
        is_error: bool = False,
    ) -> None:
        """Log a message."""
        log_method = _LOGGER.error if is_error else _LOGGER.debug
        log_method(message)
