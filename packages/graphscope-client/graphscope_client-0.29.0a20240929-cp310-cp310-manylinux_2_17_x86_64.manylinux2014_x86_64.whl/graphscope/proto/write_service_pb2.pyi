"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import request_option_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _WriteTypePb:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _WriteTypePbEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_WriteTypePb.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNKNOWN: _WriteTypePb.ValueType  # 0
    INSERT: _WriteTypePb.ValueType  # 1
    UPDATE: _WriteTypePb.ValueType  # 2
    DELETE: _WriteTypePb.ValueType  # 3
    CLEAR_PROPERTY: _WriteTypePb.ValueType  # 4

class WriteTypePb(_WriteTypePb, metaclass=_WriteTypePbEnumTypeWrapper): ...

UNKNOWN: WriteTypePb.ValueType  # 0
INSERT: WriteTypePb.ValueType  # 1
UPDATE: WriteTypePb.ValueType  # 2
DELETE: WriteTypePb.ValueType  # 3
CLEAR_PROPERTY: WriteTypePb.ValueType  # 4
global___WriteTypePb = WriteTypePb

@typing.final
class ReplayRecordsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OFFSET_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    offset: builtins.int
    timestamp: builtins.int
    def __init__(
        self,
        *,
        offset: builtins.int = ...,
        timestamp: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["offset", b"offset", "timestamp", b"timestamp"]) -> None: ...

global___ReplayRecordsRequest = ReplayRecordsRequest

@typing.final
class ReplayRecordsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SNAPSHOT_ID_FIELD_NUMBER: builtins.int
    @property
    def snapshot_id(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        snapshot_id: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["snapshot_id", b"snapshot_id"]) -> None: ...

global___ReplayRecordsResponse = ReplayRecordsResponse

@typing.final
class GetClientIdRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetClientIdRequest = GetClientIdRequest

@typing.final
class GetClientIdResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLIENT_ID_FIELD_NUMBER: builtins.int
    client_id: builtins.str
    def __init__(
        self,
        *,
        client_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["client_id", b"client_id"]) -> None: ...

global___GetClientIdResponse = GetClientIdResponse

@typing.final
class BatchWriteRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLIENT_ID_FIELD_NUMBER: builtins.int
    WRITE_REQUESTS_FIELD_NUMBER: builtins.int
    REQUEST_OPTIONS_FIELD_NUMBER: builtins.int
    client_id: builtins.str
    @property
    def write_requests(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___WriteRequestPb]: ...
    @property
    def request_options(self) -> request_option_pb2.RequestOptionsPb: ...
    def __init__(
        self,
        *,
        client_id: builtins.str = ...,
        write_requests: collections.abc.Iterable[global___WriteRequestPb] | None = ...,
        request_options: request_option_pb2.RequestOptionsPb | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["request_options", b"request_options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["client_id", b"client_id", "request_options", b"request_options", "write_requests", b"write_requests"]) -> None: ...

global___BatchWriteRequest = BatchWriteRequest

@typing.final
class BatchWriteResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SNAPSHOT_ID_FIELD_NUMBER: builtins.int
    snapshot_id: builtins.int
    def __init__(
        self,
        *,
        snapshot_id: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["snapshot_id", b"snapshot_id"]) -> None: ...

global___BatchWriteResponse = BatchWriteResponse

@typing.final
class RemoteFlushRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SNAPSHOT_ID_FIELD_NUMBER: builtins.int
    WAIT_TIME_MS_FIELD_NUMBER: builtins.int
    snapshot_id: builtins.int
    wait_time_ms: builtins.int
    def __init__(
        self,
        *,
        snapshot_id: builtins.int = ...,
        wait_time_ms: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["snapshot_id", b"snapshot_id", "wait_time_ms", b"wait_time_ms"]) -> None: ...

global___RemoteFlushRequest = RemoteFlushRequest

@typing.final
class RemoteFlushResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SUCCESS_FIELD_NUMBER: builtins.int
    success: builtins.bool
    def __init__(
        self,
        *,
        success: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["success", b"success"]) -> None: ...

global___RemoteFlushResponse = RemoteFlushResponse

@typing.final
class WriteRequestPb(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    WRITE_TYPE_FIELD_NUMBER: builtins.int
    DATA_RECORD_FIELD_NUMBER: builtins.int
    write_type: global___WriteTypePb.ValueType
    @property
    def data_record(self) -> global___DataRecordPb: ...
    def __init__(
        self,
        *,
        write_type: global___WriteTypePb.ValueType = ...,
        data_record: global___DataRecordPb | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["data_record", b"data_record"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["data_record", b"data_record", "write_type", b"write_type"]) -> None: ...

global___WriteRequestPb = WriteRequestPb

@typing.final
class DataRecordPb(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class PropertiesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    VERTEX_RECORD_KEY_FIELD_NUMBER: builtins.int
    EDGE_RECORD_KEY_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    @property
    def vertex_record_key(self) -> global___VertexRecordKeyPb: ...
    @property
    def edge_record_key(self) -> global___EdgeRecordKeyPb: ...
    @property
    def properties(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        vertex_record_key: global___VertexRecordKeyPb | None = ...,
        edge_record_key: global___EdgeRecordKeyPb | None = ...,
        properties: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["edge_record_key", b"edge_record_key", "record_key", b"record_key", "vertex_record_key", b"vertex_record_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["edge_record_key", b"edge_record_key", "properties", b"properties", "record_key", b"record_key", "vertex_record_key", b"vertex_record_key"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["record_key", b"record_key"]) -> typing.Literal["vertex_record_key", "edge_record_key"] | None: ...

global___DataRecordPb = DataRecordPb

@typing.final
class VertexRecordKeyPb(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class PkPropertiesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    LABEL_FIELD_NUMBER: builtins.int
    PK_PROPERTIES_FIELD_NUMBER: builtins.int
    label: builtins.str
    @property
    def pk_properties(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        label: builtins.str = ...,
        pk_properties: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["label", b"label", "pk_properties", b"pk_properties"]) -> None: ...

global___VertexRecordKeyPb = VertexRecordKeyPb

@typing.final
class EdgeRecordKeyPb(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LABEL_FIELD_NUMBER: builtins.int
    SRC_VERTEX_KEY_FIELD_NUMBER: builtins.int
    DST_VERTEX_KEY_FIELD_NUMBER: builtins.int
    INNER_ID_FIELD_NUMBER: builtins.int
    label: builtins.str
    inner_id: builtins.int
    @property
    def src_vertex_key(self) -> global___VertexRecordKeyPb: ...
    @property
    def dst_vertex_key(self) -> global___VertexRecordKeyPb: ...
    def __init__(
        self,
        *,
        label: builtins.str = ...,
        src_vertex_key: global___VertexRecordKeyPb | None = ...,
        dst_vertex_key: global___VertexRecordKeyPb | None = ...,
        inner_id: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["dst_vertex_key", b"dst_vertex_key", "src_vertex_key", b"src_vertex_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["dst_vertex_key", b"dst_vertex_key", "inner_id", b"inner_id", "label", b"label", "src_vertex_key", b"src_vertex_key"]) -> None: ...

global___EdgeRecordKeyPb = EdgeRecordKeyPb
