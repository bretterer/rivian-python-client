"""Offline closure encoding checks; no transport or vehicle access."""

import pytest

from rivian.parallax import encode_frunk, encode_windows
from rivian.parallax.proto import body_pb2


@pytest.mark.parametrize(
    "encoder,target,wire",
    [
        (encode_frunk, body_pb2.FRUNK, "0a0105"),
        (encode_windows, body_pb2.GROUP_WINDOWS, "0a02904e"),
    ],
)
def test_closure_target_is_exact(encoder, target, wire):
    payload = encoder()
    assert payload.hex() == wire
    decoded = body_pb2.ClosureCommand.FromString(payload)
    assert list(decoded.closure) == [target]
    assert body_pb2.LIFTGATE not in decoded.closure
    assert body_pb2.TAILGATE not in decoded.closure
