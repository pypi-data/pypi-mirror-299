# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: message.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'message.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from error import coordinator_pb2 as error_dot_coordinator__pb2
import op_def_pb2 as op__def__pb2
import types_pb2 as types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rmessage.proto\x12\x06gs.rpc\x1a\x17\x65rror/coordinator.proto\x1a\x0cop_def.proto\x1a\x0btypes.proto\"w\n\x15\x43onnectSessionRequest\x12\x18\n\x10\x63leanup_instance\x18\x01 \x01(\x08\x12 \n\x18\x64\x61ngling_timeout_seconds\x18\x02 \x01(\x05\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x11\n\treconnect\x18\x04 \x01(\x08\"\xaa\x01\n\x16\x43onnectSessionResponse\x12\x12\n\nsession_id\x18\x02 \x01(\t\x12)\n\x0c\x63luster_type\x18\x03 \x01(\x0e\x32\x13.gs.rpc.ClusterType\x12\x13\n\x0bnum_workers\x18\x06 \x01(\x05\x12\x11\n\tnamespace\x18\x07 \x01(\t\x12\x15\n\rengine_config\x18\n \x01(\t\x12\x12\n\nhost_names\x18\x0b \x03(\t\"&\n\x10HeartBeatRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"\x13\n\x11HeartBeatResponse\"I\n\x12RunStepRequestHead\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x1f\n\x07\x64\x61g_def\x18\x02 \x01(\x0b\x32\x0e.gs.rpc.DagDef\"E\n\x12RunStepRequestBody\x12\r\n\x05\x63hunk\x18\x01 \x01(\x0c\x12\x0e\n\x06op_key\x18\x02 \x01(\t\x12\x10\n\x08has_next\x18\x03 \x01(\x08\"q\n\x0eRunStepRequest\x12*\n\x04head\x18\x01 \x01(\x0b\x32\x1a.gs.rpc.RunStepRequestHeadH\x00\x12*\n\x04\x62ody\x18\x02 \x01(\x0b\x32\x1a.gs.rpc.RunStepRequestBodyH\x00\x42\x07\n\x05value\"\x7f\n\x13RunStepResponseHead\x12!\n\x07results\x18\x01 \x03(\x0b\x32\x10.gs.rpc.OpResult\x12\x1a\n\x04\x63ode\x18\x02 \x01(\x0e\x32\x0c.gs.rpc.Code\x12\x11\n\terror_msg\x18\x03 \x01(\t\x12\x16\n\x0e\x66ull_exception\x18\x04 \x01(\x0c\"6\n\x13RunStepResponseBody\x12\r\n\x05\x63hunk\x18\x01 \x01(\x0c\x12\x10\n\x08has_next\x18\x02 \x01(\x08\"t\n\x0fRunStepResponse\x12+\n\x04head\x18\x01 \x01(\x0b\x32\x1b.gs.rpc.RunStepResponseHeadH\x00\x12+\n\x04\x62ody\x18\x02 \x01(\x0b\x32\x1b.gs.rpc.RunStepResponseBodyH\x00\x42\x07\n\x05value\"&\n\x10\x46\x65tchLogsRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"@\n\x11\x46\x65tchLogsResponse\x12\x14\n\x0cinfo_message\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t\")\n\x13\x43loseSessionRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"\x16\n\x14\x43loseSessionResponse\"0\n\rAddLibRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x0b\n\x03gar\x18\x02 \x01(\x0c\"\x10\n\x0e\x41\x64\x64LibResponse\"5\n\x1f\x43reateAnalyticalInstanceRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"b\n CreateAnalyticalInstanceResponse\x12\x13\n\x0binstance_id\x18\x01 \x01(\t\x12\x15\n\rengine_config\x18\x02 \x01(\t\x12\x12\n\nhost_names\x18\x05 \x03(\t\"\xe8\x01\n CreateInteractiveInstanceRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x11\n\tobject_id\x18\x02 \x01(\x03\x12\x13\n\x0bschema_path\x18\x03 \x01(\t\x12\x44\n\x06params\x18\x04 \x03(\x0b\x32\x34.gs.rpc.CreateInteractiveInstanceRequest.ParamsEntry\x12\x13\n\x0bwith_cypher\x18\x05 \x01(\x08\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"i\n!CreateInteractiveInstanceResponse\x12\x18\n\x10gremlin_endpoint\x18\x01 \x01(\t\x12\x17\n\x0f\x63ypher_endpoint\x18\x02 \x01(\t\x12\x11\n\tobject_id\x18\x03 \x01(\x03\"\x99\x01\n\x1d\x43reateLearningInstanceRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x11\n\tobject_id\x18\x02 \x01(\x03\x12\x0e\n\x06handle\x18\x03 \x01(\t\x12\x0e\n\x06\x63onfig\x18\x04 \x01(\t\x12\x31\n\x10learning_backend\x18\x05 \x01(\x0e\x32\x17.gs.rpc.LearningBackend\"f\n\x1e\x43reateLearningInstanceResponse\x12\x11\n\tobject_id\x18\x01 \x01(\x03\x12\x0e\n\x06handle\x18\x02 \x01(\t\x12\x0e\n\x06\x63onfig\x18\x03 \x01(\t\x12\x11\n\tendpoints\x18\x04 \x03(\t\"I\n\x1e\x43loseAnalyticalInstanceRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x13\n\x0binstance_id\x18\x02 \x01(\t\"!\n\x1f\x43loseAnalyticalInstanceResponse\"H\n\x1f\x43loseInteractiveInstanceRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x11\n\tobject_id\x18\x02 \x01(\x03\"\"\n CloseInteractiveInstanceResponse\"E\n\x1c\x43loseLearningInstanceRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x11\n\tobject_id\x18\x02 \x01(\x03\"\x1f\n\x1d\x43loseLearningInstanceResponse*7\n\x0fLearningBackend\x12\x0e\n\nGRAPHLEARN\x10\x00\x12\x14\n\x10GRAPHLEARN_TORCH\x10\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'message_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATEINTERACTIVEINSTANCEREQUEST_PARAMSENTRY']._loaded_options = None
  _globals['_CREATEINTERACTIVEINSTANCEREQUEST_PARAMSENTRY']._serialized_options = b'8\001'
  _globals['_LEARNINGBACKEND']._serialized_start=2318
  _globals['_LEARNINGBACKEND']._serialized_end=2373
  _globals['_CONNECTSESSIONREQUEST']._serialized_start=77
  _globals['_CONNECTSESSIONREQUEST']._serialized_end=196
  _globals['_CONNECTSESSIONRESPONSE']._serialized_start=199
  _globals['_CONNECTSESSIONRESPONSE']._serialized_end=369
  _globals['_HEARTBEATREQUEST']._serialized_start=371
  _globals['_HEARTBEATREQUEST']._serialized_end=409
  _globals['_HEARTBEATRESPONSE']._serialized_start=411
  _globals['_HEARTBEATRESPONSE']._serialized_end=430
  _globals['_RUNSTEPREQUESTHEAD']._serialized_start=432
  _globals['_RUNSTEPREQUESTHEAD']._serialized_end=505
  _globals['_RUNSTEPREQUESTBODY']._serialized_start=507
  _globals['_RUNSTEPREQUESTBODY']._serialized_end=576
  _globals['_RUNSTEPREQUEST']._serialized_start=578
  _globals['_RUNSTEPREQUEST']._serialized_end=691
  _globals['_RUNSTEPRESPONSEHEAD']._serialized_start=693
  _globals['_RUNSTEPRESPONSEHEAD']._serialized_end=820
  _globals['_RUNSTEPRESPONSEBODY']._serialized_start=822
  _globals['_RUNSTEPRESPONSEBODY']._serialized_end=876
  _globals['_RUNSTEPRESPONSE']._serialized_start=878
  _globals['_RUNSTEPRESPONSE']._serialized_end=994
  _globals['_FETCHLOGSREQUEST']._serialized_start=996
  _globals['_FETCHLOGSREQUEST']._serialized_end=1034
  _globals['_FETCHLOGSRESPONSE']._serialized_start=1036
  _globals['_FETCHLOGSRESPONSE']._serialized_end=1100
  _globals['_CLOSESESSIONREQUEST']._serialized_start=1102
  _globals['_CLOSESESSIONREQUEST']._serialized_end=1143
  _globals['_CLOSESESSIONRESPONSE']._serialized_start=1145
  _globals['_CLOSESESSIONRESPONSE']._serialized_end=1167
  _globals['_ADDLIBREQUEST']._serialized_start=1169
  _globals['_ADDLIBREQUEST']._serialized_end=1217
  _globals['_ADDLIBRESPONSE']._serialized_start=1219
  _globals['_ADDLIBRESPONSE']._serialized_end=1235
  _globals['_CREATEANALYTICALINSTANCEREQUEST']._serialized_start=1237
  _globals['_CREATEANALYTICALINSTANCEREQUEST']._serialized_end=1290
  _globals['_CREATEANALYTICALINSTANCERESPONSE']._serialized_start=1292
  _globals['_CREATEANALYTICALINSTANCERESPONSE']._serialized_end=1390
  _globals['_CREATEINTERACTIVEINSTANCEREQUEST']._serialized_start=1393
  _globals['_CREATEINTERACTIVEINSTANCEREQUEST']._serialized_end=1625
  _globals['_CREATEINTERACTIVEINSTANCEREQUEST_PARAMSENTRY']._serialized_start=1580
  _globals['_CREATEINTERACTIVEINSTANCEREQUEST_PARAMSENTRY']._serialized_end=1625
  _globals['_CREATEINTERACTIVEINSTANCERESPONSE']._serialized_start=1627
  _globals['_CREATEINTERACTIVEINSTANCERESPONSE']._serialized_end=1732
  _globals['_CREATELEARNINGINSTANCEREQUEST']._serialized_start=1735
  _globals['_CREATELEARNINGINSTANCEREQUEST']._serialized_end=1888
  _globals['_CREATELEARNINGINSTANCERESPONSE']._serialized_start=1890
  _globals['_CREATELEARNINGINSTANCERESPONSE']._serialized_end=1992
  _globals['_CLOSEANALYTICALINSTANCEREQUEST']._serialized_start=1994
  _globals['_CLOSEANALYTICALINSTANCEREQUEST']._serialized_end=2067
  _globals['_CLOSEANALYTICALINSTANCERESPONSE']._serialized_start=2069
  _globals['_CLOSEANALYTICALINSTANCERESPONSE']._serialized_end=2102
  _globals['_CLOSEINTERACTIVEINSTANCEREQUEST']._serialized_start=2104
  _globals['_CLOSEINTERACTIVEINSTANCEREQUEST']._serialized_end=2176
  _globals['_CLOSEINTERACTIVEINSTANCERESPONSE']._serialized_start=2178
  _globals['_CLOSEINTERACTIVEINSTANCERESPONSE']._serialized_end=2212
  _globals['_CLOSELEARNINGINSTANCEREQUEST']._serialized_start=2214
  _globals['_CLOSELEARNINGINSTANCEREQUEST']._serialized_end=2283
  _globals['_CLOSELEARNINGINSTANCERESPONSE']._serialized_start=2285
  _globals['_CLOSELEARNINGINSTANCERESPONSE']._serialized_end=2316
# @@protoc_insertion_point(module_scope)
