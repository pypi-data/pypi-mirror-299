# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: groot/sdk/client_backup_service.proto
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
    'groot/sdk/client_backup_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from groot.sdk import model_pb2 as groot_dot_sdk_dot_model__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%groot/sdk/client_backup_service.proto\x12\x0cgs.rpc.groot\x1a\x15groot/sdk/model.proto\"\x1d\n\x1b\x43reateNewGraphBackupRequest\"0\n\x1c\x43reateNewGraphBackupResponse\x12\x10\n\x08\x62\x61\x63kupId\x18\x01 \x01(\x05\",\n\x18\x44\x65leteGraphBackupRequest\x12\x10\n\x08\x62\x61\x63kupId\x18\x01 \x01(\x05\"\x1b\n\x19\x44\x65leteGraphBackupResponse\"6\n\x1bPurgeOldGraphBackupsRequest\x12\x17\n\x0fkeepAliveNumber\x18\x01 \x01(\x05\"\x1e\n\x1cPurgeOldGraphBackupsResponse\"h\n\x1dRestoreFromGraphBackupRequest\x12\x10\n\x08\x62\x61\x63kupId\x18\x01 \x01(\x05\x12\x19\n\x11meta_restore_path\x18\x02 \x01(\t\x12\x1a\n\x12store_restore_path\x18\x03 \x01(\t\" \n\x1eRestoreFromGraphBackupResponse\",\n\x18VerifyGraphBackupRequest\x12\x10\n\x08\x62\x61\x63kupId\x18\x01 \x01(\x05\"9\n\x19VerifyGraphBackupResponse\x12\x0c\n\x04isOk\x18\x01 \x01(\x08\x12\x0e\n\x06\x65rrMsg\x18\x02 \x01(\t\"\x1b\n\x19GetGraphBackupInfoRequest\"P\n\x1aGetGraphBackupInfoResponse\x12\x32\n\x0e\x62\x61\x63kupInfoList\x18\x01 \x03(\x0b\x32\x1a.gs.rpc.groot.BackupInfoPb2\x96\x05\n\x0c\x43lientBackup\x12m\n\x14\x63reateNewGraphBackup\x12).gs.rpc.groot.CreateNewGraphBackupRequest\x1a*.gs.rpc.groot.CreateNewGraphBackupResponse\x12\x64\n\x11\x64\x65leteGraphBackup\x12&.gs.rpc.groot.DeleteGraphBackupRequest\x1a\'.gs.rpc.groot.DeleteGraphBackupResponse\x12m\n\x14purgeOldGraphBackups\x12).gs.rpc.groot.PurgeOldGraphBackupsRequest\x1a*.gs.rpc.groot.PurgeOldGraphBackupsResponse\x12s\n\x16restoreFromGraphBackup\x12+.gs.rpc.groot.RestoreFromGraphBackupRequest\x1a,.gs.rpc.groot.RestoreFromGraphBackupResponse\x12\x64\n\x11verifyGraphBackup\x12&.gs.rpc.groot.VerifyGraphBackupRequest\x1a\'.gs.rpc.groot.VerifyGraphBackupResponse\x12g\n\x12getGraphBackupInfo\x12\'.gs.rpc.groot.GetGraphBackupInfoRequest\x1a(.gs.rpc.groot.GetGraphBackupInfoResponseB&\n\"com.alibaba.graphscope.proto.grootP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'groot.sdk.client_backup_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.alibaba.graphscope.proto.grootP\001'
  _globals['_CREATENEWGRAPHBACKUPREQUEST']._serialized_start=78
  _globals['_CREATENEWGRAPHBACKUPREQUEST']._serialized_end=107
  _globals['_CREATENEWGRAPHBACKUPRESPONSE']._serialized_start=109
  _globals['_CREATENEWGRAPHBACKUPRESPONSE']._serialized_end=157
  _globals['_DELETEGRAPHBACKUPREQUEST']._serialized_start=159
  _globals['_DELETEGRAPHBACKUPREQUEST']._serialized_end=203
  _globals['_DELETEGRAPHBACKUPRESPONSE']._serialized_start=205
  _globals['_DELETEGRAPHBACKUPRESPONSE']._serialized_end=232
  _globals['_PURGEOLDGRAPHBACKUPSREQUEST']._serialized_start=234
  _globals['_PURGEOLDGRAPHBACKUPSREQUEST']._serialized_end=288
  _globals['_PURGEOLDGRAPHBACKUPSRESPONSE']._serialized_start=290
  _globals['_PURGEOLDGRAPHBACKUPSRESPONSE']._serialized_end=320
  _globals['_RESTOREFROMGRAPHBACKUPREQUEST']._serialized_start=322
  _globals['_RESTOREFROMGRAPHBACKUPREQUEST']._serialized_end=426
  _globals['_RESTOREFROMGRAPHBACKUPRESPONSE']._serialized_start=428
  _globals['_RESTOREFROMGRAPHBACKUPRESPONSE']._serialized_end=460
  _globals['_VERIFYGRAPHBACKUPREQUEST']._serialized_start=462
  _globals['_VERIFYGRAPHBACKUPREQUEST']._serialized_end=506
  _globals['_VERIFYGRAPHBACKUPRESPONSE']._serialized_start=508
  _globals['_VERIFYGRAPHBACKUPRESPONSE']._serialized_end=565
  _globals['_GETGRAPHBACKUPINFOREQUEST']._serialized_start=567
  _globals['_GETGRAPHBACKUPINFOREQUEST']._serialized_end=594
  _globals['_GETGRAPHBACKUPINFORESPONSE']._serialized_start=596
  _globals['_GETGRAPHBACKUPINFORESPONSE']._serialized_end=676
  _globals['_CLIENTBACKUP']._serialized_start=679
  _globals['_CLIENTBACKUP']._serialized_end=1341
# @@protoc_insertion_point(module_scope)
