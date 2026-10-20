from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PARALLAX_OPERATION_UNSPECIFIED: _ClassVar[OperationType]
    PARALLAX_OPERATION_PUBLISH: _ClassVar[OperationType]
    PARALLAX_OPERATION_SUBSCRIBE: _ClassVar[OperationType]
    PARALLAX_OPERATION_REQUEST: _ClassVar[OperationType]

class SignatureType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_SIGNATURE_TYPE_UNSPECIFIED: _ClassVar[SignatureType]
    DATA_SIGNATURE_TYPE_HMAC_SHA256: _ClassVar[SignatureType]
    DATA_SIGNATURE_TYPE_RCS: _ClassVar[SignatureType]

class Progress(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VEHICLE_MODEL_OP_PROGRESS_UNSPECIFIED: _ClassVar[Progress]
    VEHICLE_MODEL_OP_PROGRESS_VEHICLE_WAKING_UP: _ClassVar[Progress]
    VEHICLE_MODEL_OP_PROGRESS_VEHICLE_VALIDATING: _ClassVar[Progress]
    VEHICLE_MODEL_OP_PROGRESS_VEHICLE_EXECUTING: _ClassVar[Progress]
    VEHICLE_MODEL_OP_PROGRESS_VEHICLE_COMPLETE: _ClassVar[Progress]

class ResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESPONSE_STATUS_UNDEFINED: _ClassVar[ResponseStatus]
    RESPONSE_STATUS_SUCCESS: _ClassVar[ResponseStatus]
    RESPONSE_STATUS_FAIL: _ClassVar[ResponseStatus]
    RESPONSE_STATUS_INVALID_REQUEST: _ClassVar[ResponseStatus]
    RESPONSE_STATUS_NOT_SUPPORTED: _ClassVar[ResponseStatus]
    RESPONSE_STATUS_TIMEOUT: _ClassVar[ResponseStatus]
PARALLAX_OPERATION_UNSPECIFIED: OperationType
PARALLAX_OPERATION_PUBLISH: OperationType
PARALLAX_OPERATION_SUBSCRIBE: OperationType
PARALLAX_OPERATION_REQUEST: OperationType
DATA_SIGNATURE_TYPE_UNSPECIFIED: SignatureType
DATA_SIGNATURE_TYPE_HMAC_SHA256: SignatureType
DATA_SIGNATURE_TYPE_RCS: SignatureType
VEHICLE_MODEL_OP_PROGRESS_UNSPECIFIED: Progress
VEHICLE_MODEL_OP_PROGRESS_VEHICLE_WAKING_UP: Progress
VEHICLE_MODEL_OP_PROGRESS_VEHICLE_VALIDATING: Progress
VEHICLE_MODEL_OP_PROGRESS_VEHICLE_EXECUTING: Progress
VEHICLE_MODEL_OP_PROGRESS_VEHICLE_COMPLETE: Progress
RESPONSE_STATUS_UNDEFINED: ResponseStatus
RESPONSE_STATUS_SUCCESS: ResponseStatus
RESPONSE_STATUS_FAIL: ResponseStatus
RESPONSE_STATUS_INVALID_REQUEST: ResponseStatus
RESPONSE_STATUS_NOT_SUPPORTED: ResponseStatus
RESPONSE_STATUS_TIMEOUT: ResponseStatus

class Envelope(_message.Message):
    __slots__ = ("composite", "last_update", "correlation_id", "security_info")
    COMPOSITE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_INFO_FIELD_NUMBER: _ClassVar[int]
    composite: Composite
    last_update: Timestamp
    correlation_id: bytes
    security_info: SecurityInfo
    def __init__(self, composite: _Optional[_Union[Composite, _Mapping]] = ..., last_update: _Optional[_Union[Timestamp, _Mapping]] = ..., correlation_id: _Optional[bytes] = ..., security_info: _Optional[_Union[SecurityInfo, _Mapping]] = ...) -> None: ...

class Composite(_message.Message):
    __slots__ = ("bytes_val",)
    BYTES_VAL_FIELD_NUMBER: _ClassVar[int]
    bytes_val: bytes
    def __init__(self, bytes_val: _Optional[bytes] = ...) -> None: ...

class Operation(_message.Message):
    __slots__ = ("rvm", "type", "command_id", "payload", "created_at", "vehicle_id")
    RVM_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_ID_FIELD_NUMBER: _ClassVar[int]
    rvm: str
    type: OperationType
    command_id: bytes
    payload: bytes
    created_at: Timestamp
    vehicle_id: str
    def __init__(self, rvm: _Optional[str] = ..., type: _Optional[_Union[OperationType, str]] = ..., command_id: _Optional[bytes] = ..., payload: _Optional[bytes] = ..., created_at: _Optional[_Union[Timestamp, _Mapping]] = ..., vehicle_id: _Optional[str] = ...) -> None: ...

class SecurityInfo(_message.Message):
    __slots__ = ("signature", "mapped_identity")
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    MAPPED_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    signature: Signature
    mapped_identity: str
    def __init__(self, signature: _Optional[_Union[Signature, _Mapping]] = ..., mapped_identity: _Optional[str] = ...) -> None: ...

class Signature(_message.Message):
    __slots__ = ("type", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: SignatureType
    value: bytes
    def __init__(self, type: _Optional[_Union[SignatureType, str]] = ..., value: _Optional[bytes] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...

class CommandState(_message.Message):
    __slots__ = ("command_id", "rvm", "progress", "operation_error", "data")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    RVM_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    command_id: bytes
    rvm: str
    progress: Progress
    operation_error: OperationError
    data: CommandResult
    def __init__(self, command_id: _Optional[bytes] = ..., rvm: _Optional[str] = ..., progress: _Optional[_Union[Progress, str]] = ..., operation_error: _Optional[_Union[OperationError, _Mapping]] = ..., data: _Optional[_Union[CommandResult, _Mapping]] = ...) -> None: ...

class CommandResult(_message.Message):
    __slots__ = ("response_status", "error")
    RESPONSE_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    response_status: ResponseStatus
    error: Error
    def __init__(self, response_status: _Optional[_Union[ResponseStatus, str]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class OperationError(_message.Message):
    __slots__ = ("error", "message")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error: int
    message: str
    def __init__(self, error: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
