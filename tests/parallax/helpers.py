"""Shared helpers for the Parallax decoder tests.

Payloads are built from the reverse-engineered schemas in
`rivian/parallax/proto`, so each test also checks that a `.proto` file and
its decoder agree on field numbers and wire types.
"""

from __future__ import annotations

import base64
from datetime import UTC, datetime
from typing import Any

from google.protobuf.message import Message

from rivian.parallax import decode_parallax_message


def decode(rvm: str, message: Message | None = None, **kwargs: Any) -> dict[str, Any]:
    """Serialize `message` and run it through the public dispatcher."""
    data = message.SerializeToString() if message is not None else b""
    result = decode_parallax_message(rvm, base64.b64encode(data).decode(), **kwargs)
    assert result is not None
    return result


def epoch(ms: int) -> datetime:
    """A UTC datetime from epoch milliseconds, as the decoders produce."""
    return datetime.fromtimestamp(ms / 1000, UTC)
