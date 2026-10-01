"""Decoders for `gearguard_streaming.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import gearguard_streaming_pb2

_GEAR_GUARD_CONSENT_MAP: Final[dict[int, str]] = {
    0: "unrecognized",
    1: "consented",
    2: "not_consented",
    3: "not_applicable",
    4: "unknown",
}

_GEAR_GUARD_DAILY_LIMIT_MAP: Final[dict[int, str]] = {
    0: "unrecognized",
    1: "undefined",
    2: "not_hit",
    3: "hit",
}


@RVMDecoder.register(
    "gearguard_streaming.privacy.gearguard_streaming_in_vehicle_consent",
    gearguard_streaming_pb2.GearGuardStreamingConsent,
)
def decode_gearguard_streaming_consent(
    m: gearguard_streaming_pb2.GearGuardStreamingConsent,
) -> dict[str, Any]:
    """gearguard_streaming.privacy.gearguard_streaming_in_vehicle_consent — GearGuard consent.

    Fields:
        gearGuardStreamingConsent: str
            ("consented" | "not_consented" | "not_applicable" | "unknown" | "unrecognized")
    """
    if (val := _present(m, "consent")) is None:
        return {}
    return {
        "gearGuardStreamingConsent": _enum(
            _GEAR_GUARD_CONSENT_MAP, val, what="GearGuard streaming consent"
        )
    }


@RVMDecoder.register(
    "gearguard_streaming.privacy.gearguard_streaming_daily_limit",
    gearguard_streaming_pb2.GearGuardStreamingDailyLimit,
)
def decode_gearguard_streaming_daily_limit(
    m: gearguard_streaming_pb2.GearGuardStreamingDailyLimit,
) -> dict[str, Any]:
    """gearguard_streaming.privacy.gearguard_streaming_daily_limit — GearGuard daily limit.

    Fields:
        gearGuardStreamingDailyLimit: str ("not_hit" | "hit" | "undefined" | "unrecognized")
        gearGuardStreamingLimitResetTime: int (epoch seconds), when sent
    """
    result: dict[str, Any] = {}
    if (val := _present(m, "limit")) is not None:
        result["gearGuardStreamingDailyLimit"] = _enum(
            _GEAR_GUARD_DAILY_LIMIT_MAP, val, what="GearGuard streaming daily limit"
        )
    if (val := _present(m, "limit_reset_time")) is not None:
        result["gearGuardStreamingLimitResetTime"] = val
    return result
