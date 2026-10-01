"""Registry, payload parsing and shared helpers for Parallax decoders."""

from __future__ import annotations

import base64
import logging
from collections.abc import Callable
from typing import Any, ClassVar, TypeVar

from google.protobuf import text_format
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.message import Message
from google.protobuf.unknown_fields import UnknownFieldSet

from ..utils import from_epoch

_LOGGER = logging.getLogger(__name__)

_M = TypeVar("_M", bound=Message)


def _enum(
    mapping: dict[int, str],
    value: int | None,
    *,
    what: str,
    unmapped_default: str | None = None,
) -> str | int | None:
    """Map `value` through `mapping`.

    Returns None for None. An unmapped value is debug-logged and returned
    as-is, or as `unmapped_default` when given.
    """
    if value is None:
        return None
    if value in mapping:
        return mapping[value]
    _LOGGER.debug("Unknown %s value: %s", what, value)
    return value if unmapped_default is None else unmapped_default


def _present(message: Message, field: str) -> Any:
    """`message.<field>` if it was sent, else None.

    Only for fields with presence: submessages and `optional` fields.
    """
    return getattr(message, field) if message.HasField(field) else None


def _describe_unknowns(message: Message, path: str = "") -> list[str]:
    """List unknown fields and undefined enum values in `message`, recursively."""
    path = path or message.DESCRIPTOR.name
    unknown_fields = UnknownFieldSet(message)
    found = [
        f"{path}: unknown field {field.field_number} "
        f"(wire type {field.wire_type}) = {field.data!r}"
        for field in (unknown_fields[i] for i in range(len(unknown_fields)))
    ]
    for desc in message.DESCRIPTOR.fields:
        field_path = f"{path}.{desc.name}"
        value = getattr(message, desc.name)
        values = list(value) if desc.is_repeated else [value]
        if desc.type == FieldDescriptor.TYPE_ENUM and desc.enum_type is not None:
            known = desc.enum_type.values_by_number
            found += [
                f"{field_path}: unknown {desc.enum_type.name} value {v}"
                for v in values
                if v not in known
            ]
        elif desc.type == FieldDescriptor.TYPE_MESSAGE:
            if desc.is_repeated:
                for index, item in enumerate(values):
                    found += _describe_unknowns(item, f"{field_path}[{index}]")
            elif message.HasField(desc.name):
                found += _describe_unknowns(value, field_path)
    return found


class RVMDecoder:
    """Registry of RVM topic -> (message class, decoder).

    The decoder receives the payload parsed as its message class.
    """

    decoders: ClassVar[dict[str, Callable[[Any], dict[str, Any]]]] = {}
    messages: ClassVar[dict[str, type[Message]]] = {}

    @classmethod
    def register(
        cls, rvm: str, message: type[_M]
    ) -> Callable[[Callable[[_M], dict[str, Any]]], Callable[[_M], dict[str, Any]]]:
        """Register the decorated function as `rvm`'s decoder.

        Raises `ValueError` if `rvm` already has one.
        """

        def wrap(
            func: Callable[[_M], dict[str, Any]],
        ) -> Callable[[_M], dict[str, Any]]:
            if rvm in cls.decoders:
                raise ValueError(
                    f"RVM {rvm!r} is already registered to "
                    f"{cls.decoders[rvm].__qualname__!r}; "
                    f"cannot also register {func.__qualname__!r}"
                )
            cls.decoders[rvm] = func
            cls.messages[rvm] = message
            return func

        return wrap


def _decode_rvm_payload(payload: str | None, rvm: str) -> dict[str, Any]:
    """Parse a base64 `payload` and run `rvm`'s decoder; {} on failure.

    An empty payload still runs the decoder, as an all-defaults message.
    Debug-logs the parsed message and anything its schema doesn't define.
    """
    if payload is None:
        return {}
    try:
        message = RVMDecoder.messages[rvm].FromString(base64.b64decode(payload))
        result = RVMDecoder.decoders[rvm](message)
    except Exception:
        _LOGGER.debug("Failed to decode %s payload", rvm, exc_info=True)
        return {}
    if _LOGGER.isEnabledFor(logging.DEBUG):
        _LOGGER.debug(
            "%s: %s", rvm, text_format.MessageToString(message, as_one_line=True)
        )
        for unknown in _describe_unknowns(message):
            _LOGGER.debug("%s: %s", rvm, unknown)
    return result


def decode_parallax_message(
    rvm: str, payload: str, timestamp: float | None = None, **kwargs: Any
) -> dict[str, Any] | None:
    """Decode a Parallax message's payload by its RVM topic.

    Takes the GraphQL message's fields as keyword arguments (extra ones
    are ignored). A `timestamp` (epoch milliseconds) is added to the
    result as a UTC datetime. Returns None for an RVM with no decoder.
    """
    if rvm not in RVMDecoder.decoders:
        _LOGGER.debug("No decoder for Parallax RVM topic %s", rvm)
        return None
    result = _decode_rvm_payload(payload, rvm)
    if timestamp is not None:
        result["timestamp"] = from_epoch(timestamp)
    return result


def decode_parallax_subscription_message(data: dict[str, Any]) -> dict[str, Any] | None:
    """Decode a raw `subscribe_for_parallax_messages` message.

    Unwraps `payload.data.parallaxMessages`; returns None if it's missing
    (e.g. an error frame) or its RVM has no decoder.
    """
    message = ((data.get("payload") or {}).get("data") or {}).get("parallaxMessages")
    if not message:
        return None
    return decode_parallax_message(**message)
