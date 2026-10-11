from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATION_READ: _ClassVar[OperationType]
    OPERATION_WRITE: _ClassVar[OperationType]
OPERATION_READ: OperationType
OPERATION_WRITE: OperationType

class VehicleOperationRequest(_message.Message):
    __slots__ = ("metadata", "operation")
    class Metadata(_message.Message):
        __slots__ = ("phone_info", "request_id")
        class PhoneInfo(_message.Message):
            __slots__ = ("field_1", "phone_id")
            FIELD_1_FIELD_NUMBER: _ClassVar[int]
            PHONE_ID_FIELD_NUMBER: _ClassVar[int]
            field_1: int
            phone_id: bytes
            def __init__(self, field_1: _Optional[int] = ..., phone_id: _Optional[bytes] = ...) -> None: ...
        PHONE_INFO_FIELD_NUMBER: _ClassVar[int]
        REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
        phone_info: VehicleOperationRequest.Metadata.PhoneInfo
        request_id: str
        def __init__(self, phone_info: _Optional[_Union[VehicleOperationRequest.Metadata.PhoneInfo, _Mapping]] = ..., request_id: _Optional[str] = ...) -> None: ...
    class Operation(_message.Message):
        __slots__ = ("rvm", "type", "payload")
        RVM_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_FIELD_NUMBER: _ClassVar[int]
        rvm: str
        type: OperationType
        payload: bytes
        def __init__(self, rvm: _Optional[str] = ..., type: _Optional[_Union[OperationType, str]] = ..., payload: _Optional[bytes] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    metadata: VehicleOperationRequest.Metadata
    operation: VehicleOperationRequest.Operation
    def __init__(self, metadata: _Optional[_Union[VehicleOperationRequest.Metadata, _Mapping]] = ..., operation: _Optional[_Union[VehicleOperationRequest.Operation, _Mapping]] = ...) -> None: ...
