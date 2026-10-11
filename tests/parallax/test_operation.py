"""Tests for the `sendVehicleOperation` request encoder."""

from __future__ import annotations

import base64

from rivian.parallax import encode_vehicle_operation
from rivian.parallax.proto import operation_pb2 as operation

RVM = "comfort.cabin.climate_hold_setting"


def _request(encoded: str) -> operation.VehicleOperationRequest:
    return operation.VehicleOperationRequest.FromString(base64.b64decode(encoded))


def test_encode_write() -> None:
    """A payload makes the request a write."""
    request = _request(
        encode_vehicle_operation(RVM, b"\x08\xa0\x38", request_id="request-id")
    )
    assert request.metadata.phone_info.field_1 == 1
    assert request.metadata.phone_info.phone_id == bytes(16)
    assert request.metadata.request_id == "request-id"
    assert request.operation.rvm == RVM
    assert request.operation.type == operation.OPERATION_WRITE
    assert request.operation.payload == b"\x08\xa0\x38"


def test_encode_read() -> None:
    """No payload makes it a read, whose type is still sent."""
    request = _request(encode_vehicle_operation(RVM, phone_id=b"\x01" * 16))
    assert request.metadata.phone_info.phone_id == b"\x01" * 16
    assert len(request.metadata.request_id) == 36
    assert request.operation.rvm == RVM
    assert request.operation.HasField("type")
    assert request.operation.type == operation.OPERATION_READ
    assert request.operation.payload == b""
