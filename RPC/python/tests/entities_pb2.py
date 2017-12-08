# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tests/entities.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from onedrive_client.RPC import RPC_pb2 as onedrive__client_dot_RPC_dot_RPC__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tests/entities.proto',
  package='tests.entities',
  syntax='proto3',
  serialized_pb=_b('\n\x14tests/entities.proto\x12\x0etests.entities\x1a\x1donedrive_client/RPC/RPC.proto\"\x13\n\x03\x46oo\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1a\n\nBarRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1b\n\x0b\x42\x61rResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\tb\x06proto3')
  ,
  dependencies=[onedrive__client_dot_RPC_dot_RPC__pb2.DESCRIPTOR,])




_FOO = _descriptor.Descriptor(
  name='Foo',
  full_name='tests.entities.Foo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='tests.entities.Foo.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=71,
  serialized_end=90,
)


_BARREQUEST = _descriptor.Descriptor(
  name='BarRequest',
  full_name='tests.entities.BarRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='tests.entities.BarRequest.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=92,
  serialized_end=118,
)


_BARRESPONSE = _descriptor.Descriptor(
  name='BarResponse',
  full_name='tests.entities.BarResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='tests.entities.BarResponse.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=147,
)

DESCRIPTOR.message_types_by_name['Foo'] = _FOO
DESCRIPTOR.message_types_by_name['BarRequest'] = _BARREQUEST
DESCRIPTOR.message_types_by_name['BarResponse'] = _BARRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Foo = _reflection.GeneratedProtocolMessageType('Foo', (_message.Message,), dict(
  DESCRIPTOR = _FOO,
  __module__ = 'tests.entities_pb2'
  # @@protoc_insertion_point(class_scope:tests.entities.Foo)
  ))
_sym_db.RegisterMessage(Foo)

BarRequest = _reflection.GeneratedProtocolMessageType('BarRequest', (_message.Message,), dict(
  DESCRIPTOR = _BARREQUEST,
  __module__ = 'tests.entities_pb2'
  # @@protoc_insertion_point(class_scope:tests.entities.BarRequest)
  ))
_sym_db.RegisterMessage(BarRequest)

BarResponse = _reflection.GeneratedProtocolMessageType('BarResponse', (_message.Message,), dict(
  DESCRIPTOR = _BARRESPONSE,
  __module__ = 'tests.entities_pb2'
  # @@protoc_insertion_point(class_scope:tests.entities.BarResponse)
  ))
_sym_db.RegisterMessage(BarResponse)


# @@protoc_insertion_point(module_scope)
