"""Encoder for `sendVehicleOperation` requests."""

from __future__ import annotations

import base64
import uuid

from .proto import operation_pb2

_Request = operation_pb2.VehicleOperationRequest


def encode_vehicle_operation(
    rvm: str,
    payload: bytes = b"",
    phone_id: bytes = bytes(16),
    request_id: str | None = None,
) -> str:
    """Encode a `sendVehicleOperation` request as a base64 string.

    An empty payload asks the vehicle to publish the current value of the RVM,
    anything else writes it. The vehicle accepts an all-zero phone id.
    """
    request = _Request(
        metadata=_Request.Metadata(
            phone_info=_Request.Metadata.PhoneInfo(field_1=1, phone_id=phone_id),
            request_id=request_id or str(uuid.uuid4()),
        ),
        operation=_Request.Operation(
            rvm=rvm,
            type=(
                operation_pb2.OPERATION_WRITE
                if payload
                else operation_pb2.OPERATION_READ
            ),
            payload=payload,
        ),
    )
    return base64.b64encode(request.SerializeToString()).decode("utf-8")
