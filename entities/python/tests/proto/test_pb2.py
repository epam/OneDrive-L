# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tests/proto/test.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tests/proto/test.proto',
  package='tests.proto.test',
  syntax='proto3',
  serialized_pb=_b('\n\x16tests/proto/test.proto\x12\x10tests.proto.test\"\x13\n\x03\x42\x61r\x12\x0c\n\x04\x65ggs\x18\x01 \x01(\r\"\x8c\x03\n\x03\x46oo\x12\x0b\n\x03\x66oo\x18\x01 \x01(\x0c\x12\x16\n\x0erepeated_field\x18\x02 \x03(\t\x12.\n\x0f\x63omposite_field\x18\x03 \x01(\x0b\x32\x15.tests.proto.test.Bar\x12\r\n\x03\x62\x61r\x18\x04 \x01(\tH\x00\x12\r\n\x03\x62\x61z\x18\x05 \x01(\x04H\x00\x12%\n\x04spam\x18\x06 \x01(\x0b\x32\x15.tests.proto.test.BarH\x00\x12\x30\n\x06\x61zerty\x18\x07 \x01(\x0b\x32 .tests.proto.test.Foo.SubMessage\x12\x37\n\x0cmanufacturer\x18\x08 \x01(\x0e\x32!.tests.proto.test.CarManufacturer\x12\x35\n\x0esub_enum_field\x18\t \x01(\x0e\x32\x1d.tests.proto.test.Foo.SubEnum\x1a\x1e\n\nSubMessage\x12\x10\n\x08sausages\x18\x01 \x01(\x11\"\x1b\n\x07SubEnum\x12\x07\n\x03\x46OO\x10\x00\x12\x07\n\x03\x42\x41R\x10\x01\x42\x0c\n\ntest_oneof*5\n\x0f\x43\x61rManufacturer\x12\x08\n\x04\x41UDI\x10\x00\x12\x0c\n\x08MERCEDES\x10\x01\x12\n\n\x06TOYOTA\x10\x02\x62\x06proto3')
)

_CARMANUFACTURER = _descriptor.EnumDescriptor(
  name='CarManufacturer',
  full_name='tests.proto.test.CarManufacturer',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AUDI', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MERCEDES', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOYOTA', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=464,
  serialized_end=517,
)
_sym_db.RegisterEnumDescriptor(_CARMANUFACTURER)

CarManufacturer = enum_type_wrapper.EnumTypeWrapper(_CARMANUFACTURER)
AUDI = 0
MERCEDES = 1
TOYOTA = 2


_FOO_SUBENUM = _descriptor.EnumDescriptor(
  name='SubEnum',
  full_name='tests.proto.test.Foo.SubEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FOO', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAR', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=421,
  serialized_end=448,
)
_sym_db.RegisterEnumDescriptor(_FOO_SUBENUM)


_BAR = _descriptor.Descriptor(
  name='Bar',
  full_name='tests.proto.test.Bar',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='eggs', full_name='tests.proto.test.Bar.eggs', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=44,
  serialized_end=63,
)


_FOO_SUBMESSAGE = _descriptor.Descriptor(
  name='SubMessage',
  full_name='tests.proto.test.Foo.SubMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sausages', full_name='tests.proto.test.Foo.SubMessage.sausages', index=0,
      number=1, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=389,
  serialized_end=419,
)

_FOO = _descriptor.Descriptor(
  name='Foo',
  full_name='tests.proto.test.Foo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foo', full_name='tests.proto.test.Foo.foo', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_field', full_name='tests.proto.test.Foo.repeated_field', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='composite_field', full_name='tests.proto.test.Foo.composite_field', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bar', full_name='tests.proto.test.Foo.bar', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='baz', full_name='tests.proto.test.Foo.baz', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='spam', full_name='tests.proto.test.Foo.spam', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='azerty', full_name='tests.proto.test.Foo.azerty', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='manufacturer', full_name='tests.proto.test.Foo.manufacturer', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sub_enum_field', full_name='tests.proto.test.Foo.sub_enum_field', index=8,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_FOO_SUBMESSAGE, ],
  enum_types=[
    _FOO_SUBENUM,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='test_oneof', full_name='tests.proto.test.Foo.test_oneof',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=66,
  serialized_end=462,
)

_FOO_SUBMESSAGE.containing_type = _FOO
_FOO.fields_by_name['composite_field'].message_type = _BAR
_FOO.fields_by_name['spam'].message_type = _BAR
_FOO.fields_by_name['azerty'].message_type = _FOO_SUBMESSAGE
_FOO.fields_by_name['manufacturer'].enum_type = _CARMANUFACTURER
_FOO.fields_by_name['sub_enum_field'].enum_type = _FOO_SUBENUM
_FOO_SUBENUM.containing_type = _FOO
_FOO.oneofs_by_name['test_oneof'].fields.append(
  _FOO.fields_by_name['bar'])
_FOO.fields_by_name['bar'].containing_oneof = _FOO.oneofs_by_name['test_oneof']
_FOO.oneofs_by_name['test_oneof'].fields.append(
  _FOO.fields_by_name['baz'])
_FOO.fields_by_name['baz'].containing_oneof = _FOO.oneofs_by_name['test_oneof']
_FOO.oneofs_by_name['test_oneof'].fields.append(
  _FOO.fields_by_name['spam'])
_FOO.fields_by_name['spam'].containing_oneof = _FOO.oneofs_by_name['test_oneof']
DESCRIPTOR.message_types_by_name['Bar'] = _BAR
DESCRIPTOR.message_types_by_name['Foo'] = _FOO
DESCRIPTOR.enum_types_by_name['CarManufacturer'] = _CARMANUFACTURER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Bar = _reflection.GeneratedProtocolMessageType('Bar', (_message.Message,), dict(
  DESCRIPTOR = _BAR,
  __module__ = 'tests.proto.test_pb2'
  # @@protoc_insertion_point(class_scope:tests.proto.test.Bar)
  ))
_sym_db.RegisterMessage(Bar)

Foo = _reflection.GeneratedProtocolMessageType('Foo', (_message.Message,), dict(

  SubMessage = _reflection.GeneratedProtocolMessageType('SubMessage', (_message.Message,), dict(
    DESCRIPTOR = _FOO_SUBMESSAGE,
    __module__ = 'tests.proto.test_pb2'
    # @@protoc_insertion_point(class_scope:tests.proto.test.Foo.SubMessage)
    ))
  ,
  DESCRIPTOR = _FOO,
  __module__ = 'tests.proto.test_pb2'
  # @@protoc_insertion_point(class_scope:tests.proto.test.Foo)
  ))
_sym_db.RegisterMessage(Foo)
_sym_db.RegisterMessage(Foo.SubMessage)


# @@protoc_insertion_point(module_scope)