# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: xee.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\txee.proto\"\x07\n\x05\x45mpty\"+\n\x0cPostXeetData\x12\r\n\x05token\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"\x1c\n\x08\x41uthData\x12\x10\n\x08username\x18\x01 \x01(\t\"\x1c\n\x0b\x41uthDetails\x12\r\n\x05token\x18\x01 \x01(\t\"(\n\x08UserData\x12\x12\n\x05token\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_token\"R\n\x08XeetData\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06poster\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\r\n\x05liked\x18\x04 \x01(\x08\x12\r\n\x05likes\x18\x05 \x01(\x05\"\x1f\n\x04\x46\x65\x65\x64\x12\x17\n\x04\x66\x65\x65\x64\x18\x01 \x03(\x0b\x32\t.XeetData\"9\n\x08LikeData\x12\r\n\x05token\x18\x01 \x01(\t\x12\x0f\n\x07xeet_id\x18\x02 \x01(\t\x12\r\n\x05liked\x18\x03 \x01(\x08\",\n\nLikeUpdate\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\r\n\x05likes\x18\x02 \x01(\x05\x32+\n\x06Poster\x12!\n\x08PostXeet\x12\r.PostXeetData\x1a\x06.Empty2V\n\rAuthenticator\x12#\n\x08\x41uthUser\x12\t.AuthData\x1a\x0c.AuthDetails\x12 \n\x0bRevokeToken\x12\t.UserData\x1a\x06.Empty2-\n\tRetriever\x12 \n\x0cRetrieveFeed\x12\t.UserData\x1a\x05.Feed2\'\n\x05Liker\x12\x1e\n\x04Like\x12\t.LikeData\x1a\x0b.LikeUpdateb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'xee_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=13
  _globals['_EMPTY']._serialized_end=20
  _globals['_POSTXEETDATA']._serialized_start=22
  _globals['_POSTXEETDATA']._serialized_end=65
  _globals['_AUTHDATA']._serialized_start=67
  _globals['_AUTHDATA']._serialized_end=95
  _globals['_AUTHDETAILS']._serialized_start=97
  _globals['_AUTHDETAILS']._serialized_end=125
  _globals['_USERDATA']._serialized_start=127
  _globals['_USERDATA']._serialized_end=167
  _globals['_XEETDATA']._serialized_start=169
  _globals['_XEETDATA']._serialized_end=251
  _globals['_FEED']._serialized_start=253
  _globals['_FEED']._serialized_end=284
  _globals['_LIKEDATA']._serialized_start=286
  _globals['_LIKEDATA']._serialized_end=343
  _globals['_LIKEUPDATE']._serialized_start=345
  _globals['_LIKEUPDATE']._serialized_end=389
  _globals['_POSTER']._serialized_start=391
  _globals['_POSTER']._serialized_end=434
  _globals['_AUTHENTICATOR']._serialized_start=436
  _globals['_AUTHENTICATOR']._serialized_end=522
  _globals['_RETRIEVER']._serialized_start=524
  _globals['_RETRIEVER']._serialized_end=569
  _globals['_LIKER']._serialized_start=571
  _globals['_LIKER']._serialized_end=610
# @@protoc_insertion_point(module_scope)
