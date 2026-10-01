"""Tests for the `security.*` decoders."""

from __future__ import annotations

from rivian.parallax.proto import security_pb2 as security

from .helpers import decode


def test_passive_entry_debug() -> None:
    """The unlock fail reason maps to its enum string."""
    result = decode(
        "security.access.passive_entry_debug",
        security.PassiveEntryDebug(reason=security.PASSIVE_ENTRY_AT_HOME_DISABLE),
    )
    assert result == {"passiveEntryUnlockFailReason": "at_home_disable"}
