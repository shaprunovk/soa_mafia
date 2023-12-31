# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngame.proto\x12\x04grpc\"\x07\n\x05\x45mpty\"h\n\x07Message\x12\x16\n\tplayer_id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x11\n\x04name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\n\n\x02to\x18\x04 \x03(\x05\x42\x0c\n\n_player_idB\x07\n\x05_name\"\x1e\n\nConnection\x12\x10\n\x08nickname\x18\x01 \x01(\t\"$\n\x0f\x43onnectionReply\x12\x11\n\tplayer_id\x18\x01 \x01(\x05\x32\x97\x01\n\nGameServer\x12*\n\nGameStream\x12\x0b.grpc.Empty\x1a\r.grpc.Message0\x01\x12)\n\x0bSendMessage\x12\r.grpc.Message\x1a\x0b.grpc.Empty\x12\x32\n\x07\x43onnect\x12\x10.grpc.Connection\x1a\x15.grpc.ConnectionReplyb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_CONNECTION = DESCRIPTOR.message_types_by_name['Connection']
_CONNECTIONREPLY = DESCRIPTOR.message_types_by_name['ConnectionReply']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'game_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Empty)
  })
_sym_db.RegisterMessage(Empty)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'game_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Message)
  })
_sym_db.RegisterMessage(Message)

Connection = _reflection.GeneratedProtocolMessageType('Connection', (_message.Message,), {
  'DESCRIPTOR' : _CONNECTION,
  '__module__' : 'game_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Connection)
  })
_sym_db.RegisterMessage(Connection)

ConnectionReply = _reflection.GeneratedProtocolMessageType('ConnectionReply', (_message.Message,), {
  'DESCRIPTOR' : _CONNECTIONREPLY,
  '__module__' : 'game_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ConnectionReply)
  })
_sym_db.RegisterMessage(ConnectionReply)

_GAMESERVER = DESCRIPTOR.services_by_name['GameServer']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=20
  _EMPTY._serialized_end=27
  _MESSAGE._serialized_start=29
  _MESSAGE._serialized_end=133
  _CONNECTION._serialized_start=135
  _CONNECTION._serialized_end=165
  _CONNECTIONREPLY._serialized_start=167
  _CONNECTIONREPLY._serialized_end=203
  _GAMESERVER._serialized_start=206
  _GAMESERVER._serialized_end=357
# @@protoc_insertion_point(module_scope)
