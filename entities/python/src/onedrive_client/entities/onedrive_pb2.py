# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: onedrive_client/entities/onedrive.proto

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
  name='onedrive_client/entities/onedrive.proto',
  package='onedrive_client.entities.onedrive',
  syntax='proto3',
  serialized_pb=_b('\n\'onedrive_client/entities/onedrive.proto\x12!onedrive_client.entities.onedrive\"c\n\x08\x42\x61seItem\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\r\n\x05\x65_tag\x18\x02 \x01(\x0c\x12\r\n\x05\x63_tag\x18\x03 \x01(\x0c\x12\x1f\n\x17last_modified_date_time\x18\x04 \x01(\x04\x12\x0c\n\x04name\x18\x05 \x01(\t\"\x89\x01\n\x05\x44rive\x12>\n\tbase_item\x18\x01 \x01(\x0b\x32+.onedrive_client.entities.onedrive.BaseItem\x12@\n\ndrive_type\x18\x02 \x01(\x0e\x32,.onedrive_client.entities.onedrive.DriveType\"\r\n\x0b\x46olderFacet\"\x0e\n\x0cPackageFacet\"\x0e\n\x0c\x44\x65letedFacet\"L\n\x0bHashesFacet\x12\x12\n\ncrc32_hash\x18\x01 \x01(\x0c\x12\x11\n\tsha1_hash\x18\x02 \x01(\x0c\x12\x16\n\x0equick_xor_hash\x18\x03 \x01(\x0c\"K\n\tFileFacet\x12>\n\x06hashes\x18\x01 \x01(\x0b\x32..onedrive_client.entities.onedrive.HashesFacet\"\xd4\x02\n\x04Item\x12>\n\tbase_item\x18\x01 \x01(\x0b\x32+.onedrive_client.entities.onedrive.BaseItem\x12\x0c\n\x04size\x18\x02 \x01(\x04\x12:\n\x04\x66ile\x18\x03 \x01(\x0b\x32,.onedrive_client.entities.onedrive.FileFacet\x12>\n\x06\x66older\x18\x04 \x01(\x0b\x32..onedrive_client.entities.onedrive.FolderFacet\x12@\n\x07package\x18\x05 \x01(\x0b\x32/.onedrive_client.entities.onedrive.PackageFacet\x12@\n\x07\x64\x65leted\x18\x06 \x01(\x0b\x32/.onedrive_client.entities.onedrive.DeletedFacet\"/\n\rExpectedRange\x12\x11\n\tbeginning\x18\x01 \x01(\r\x12\x0b\n\x03\x65nd\x18\x02 \x01(\r\"|\n\x0cUploadStatus\x12\x1c\n\x14\x65xpiration_date_time\x18\x01 \x01(\x04\x12N\n\x14next_expected_ranges\x18\x02 \x03(\x0b\x32\x30.onedrive_client.entities.onedrive.ExpectedRange\"6\n\x0cUploadedFile\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04size\x18\x03 \x01(\x04*=\n\tDriveType\x12\x0c\n\x08PERSONAL\x10\x00\x12\x0c\n\x08\x42USINESS\x10\x01\x12\x14\n\x10\x44OCUMENT_LIBRARY\x10\x02*5\n\x10\x43onflictBehavior\x12\n\n\x06RENAME\x10\x00\x12\x0b\n\x07REPLACE\x10\x01\x12\x08\n\x04\x46\x41IL\x10\x02\x62\x06proto3')
)

_DRIVETYPE = _descriptor.EnumDescriptor(
  name='DriveType',
  full_name='onedrive_client.entities.onedrive.DriveType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PERSONAL', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUSINESS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOCUMENT_LIBRARY', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1095,
  serialized_end=1156,
)
_sym_db.RegisterEnumDescriptor(_DRIVETYPE)

DriveType = enum_type_wrapper.EnumTypeWrapper(_DRIVETYPE)
_CONFLICTBEHAVIOR = _descriptor.EnumDescriptor(
  name='ConflictBehavior',
  full_name='onedrive_client.entities.onedrive.ConflictBehavior',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RENAME', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REPLACE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAIL', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1158,
  serialized_end=1211,
)
_sym_db.RegisterEnumDescriptor(_CONFLICTBEHAVIOR)

ConflictBehavior = enum_type_wrapper.EnumTypeWrapper(_CONFLICTBEHAVIOR)
PERSONAL = 0
BUSINESS = 1
DOCUMENT_LIBRARY = 2
RENAME = 0
REPLACE = 1
FAIL = 2



_BASEITEM = _descriptor.Descriptor(
  name='BaseItem',
  full_name='onedrive_client.entities.onedrive.BaseItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='onedrive_client.entities.onedrive.BaseItem.id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='e_tag', full_name='onedrive_client.entities.onedrive.BaseItem.e_tag', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='c_tag', full_name='onedrive_client.entities.onedrive.BaseItem.c_tag', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_modified_date_time', full_name='onedrive_client.entities.onedrive.BaseItem.last_modified_date_time', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='onedrive_client.entities.onedrive.BaseItem.name', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=78,
  serialized_end=177,
)


_DRIVE = _descriptor.Descriptor(
  name='Drive',
  full_name='onedrive_client.entities.onedrive.Drive',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_item', full_name='onedrive_client.entities.onedrive.Drive.base_item', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drive_type', full_name='onedrive_client.entities.onedrive.Drive.drive_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
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
  serialized_start=180,
  serialized_end=317,
)


_FOLDERFACET = _descriptor.Descriptor(
  name='FolderFacet',
  full_name='onedrive_client.entities.onedrive.FolderFacet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=319,
  serialized_end=332,
)


_PACKAGEFACET = _descriptor.Descriptor(
  name='PackageFacet',
  full_name='onedrive_client.entities.onedrive.PackageFacet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=334,
  serialized_end=348,
)


_DELETEDFACET = _descriptor.Descriptor(
  name='DeletedFacet',
  full_name='onedrive_client.entities.onedrive.DeletedFacet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=350,
  serialized_end=364,
)


_HASHESFACET = _descriptor.Descriptor(
  name='HashesFacet',
  full_name='onedrive_client.entities.onedrive.HashesFacet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='crc32_hash', full_name='onedrive_client.entities.onedrive.HashesFacet.crc32_hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sha1_hash', full_name='onedrive_client.entities.onedrive.HashesFacet.sha1_hash', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='quick_xor_hash', full_name='onedrive_client.entities.onedrive.HashesFacet.quick_xor_hash', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=366,
  serialized_end=442,
)


_FILEFACET = _descriptor.Descriptor(
  name='FileFacet',
  full_name='onedrive_client.entities.onedrive.FileFacet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hashes', full_name='onedrive_client.entities.onedrive.FileFacet.hashes', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=444,
  serialized_end=519,
)


_ITEM = _descriptor.Descriptor(
  name='Item',
  full_name='onedrive_client.entities.onedrive.Item',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_item', full_name='onedrive_client.entities.onedrive.Item.base_item', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='onedrive_client.entities.onedrive.Item.size', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='file', full_name='onedrive_client.entities.onedrive.Item.file', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='folder', full_name='onedrive_client.entities.onedrive.Item.folder', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='package', full_name='onedrive_client.entities.onedrive.Item.package', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='deleted', full_name='onedrive_client.entities.onedrive.Item.deleted', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=522,
  serialized_end=862,
)


_EXPECTEDRANGE = _descriptor.Descriptor(
  name='ExpectedRange',
  full_name='onedrive_client.entities.onedrive.ExpectedRange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='beginning', full_name='onedrive_client.entities.onedrive.ExpectedRange.beginning', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end', full_name='onedrive_client.entities.onedrive.ExpectedRange.end', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=864,
  serialized_end=911,
)


_UPLOADSTATUS = _descriptor.Descriptor(
  name='UploadStatus',
  full_name='onedrive_client.entities.onedrive.UploadStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='expiration_date_time', full_name='onedrive_client.entities.onedrive.UploadStatus.expiration_date_time', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='next_expected_ranges', full_name='onedrive_client.entities.onedrive.UploadStatus.next_expected_ranges', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=913,
  serialized_end=1037,
)


_UPLOADEDFILE = _descriptor.Descriptor(
  name='UploadedFile',
  full_name='onedrive_client.entities.onedrive.UploadedFile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='onedrive_client.entities.onedrive.UploadedFile.id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='onedrive_client.entities.onedrive.UploadedFile.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='onedrive_client.entities.onedrive.UploadedFile.size', index=2,
      number=3, type=4, cpp_type=4, label=1,
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
  serialized_start=1039,
  serialized_end=1093,
)

_DRIVE.fields_by_name['base_item'].message_type = _BASEITEM
_DRIVE.fields_by_name['drive_type'].enum_type = _DRIVETYPE
_FILEFACET.fields_by_name['hashes'].message_type = _HASHESFACET
_ITEM.fields_by_name['base_item'].message_type = _BASEITEM
_ITEM.fields_by_name['file'].message_type = _FILEFACET
_ITEM.fields_by_name['folder'].message_type = _FOLDERFACET
_ITEM.fields_by_name['package'].message_type = _PACKAGEFACET
_ITEM.fields_by_name['deleted'].message_type = _DELETEDFACET
_UPLOADSTATUS.fields_by_name['next_expected_ranges'].message_type = _EXPECTEDRANGE
DESCRIPTOR.message_types_by_name['BaseItem'] = _BASEITEM
DESCRIPTOR.message_types_by_name['Drive'] = _DRIVE
DESCRIPTOR.message_types_by_name['FolderFacet'] = _FOLDERFACET
DESCRIPTOR.message_types_by_name['PackageFacet'] = _PACKAGEFACET
DESCRIPTOR.message_types_by_name['DeletedFacet'] = _DELETEDFACET
DESCRIPTOR.message_types_by_name['HashesFacet'] = _HASHESFACET
DESCRIPTOR.message_types_by_name['FileFacet'] = _FILEFACET
DESCRIPTOR.message_types_by_name['Item'] = _ITEM
DESCRIPTOR.message_types_by_name['ExpectedRange'] = _EXPECTEDRANGE
DESCRIPTOR.message_types_by_name['UploadStatus'] = _UPLOADSTATUS
DESCRIPTOR.message_types_by_name['UploadedFile'] = _UPLOADEDFILE
DESCRIPTOR.enum_types_by_name['DriveType'] = _DRIVETYPE
DESCRIPTOR.enum_types_by_name['ConflictBehavior'] = _CONFLICTBEHAVIOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BaseItem = _reflection.GeneratedProtocolMessageType('BaseItem', (_message.Message,), dict(
  DESCRIPTOR = _BASEITEM,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.BaseItem)
  ))
_sym_db.RegisterMessage(BaseItem)

Drive = _reflection.GeneratedProtocolMessageType('Drive', (_message.Message,), dict(
  DESCRIPTOR = _DRIVE,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.Drive)
  ))
_sym_db.RegisterMessage(Drive)

FolderFacet = _reflection.GeneratedProtocolMessageType('FolderFacet', (_message.Message,), dict(
  DESCRIPTOR = _FOLDERFACET,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.FolderFacet)
  ))
_sym_db.RegisterMessage(FolderFacet)

PackageFacet = _reflection.GeneratedProtocolMessageType('PackageFacet', (_message.Message,), dict(
  DESCRIPTOR = _PACKAGEFACET,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.PackageFacet)
  ))
_sym_db.RegisterMessage(PackageFacet)

DeletedFacet = _reflection.GeneratedProtocolMessageType('DeletedFacet', (_message.Message,), dict(
  DESCRIPTOR = _DELETEDFACET,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.DeletedFacet)
  ))
_sym_db.RegisterMessage(DeletedFacet)

HashesFacet = _reflection.GeneratedProtocolMessageType('HashesFacet', (_message.Message,), dict(
  DESCRIPTOR = _HASHESFACET,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.HashesFacet)
  ))
_sym_db.RegisterMessage(HashesFacet)

FileFacet = _reflection.GeneratedProtocolMessageType('FileFacet', (_message.Message,), dict(
  DESCRIPTOR = _FILEFACET,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.FileFacet)
  ))
_sym_db.RegisterMessage(FileFacet)

Item = _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), dict(
  DESCRIPTOR = _ITEM,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.Item)
  ))
_sym_db.RegisterMessage(Item)

ExpectedRange = _reflection.GeneratedProtocolMessageType('ExpectedRange', (_message.Message,), dict(
  DESCRIPTOR = _EXPECTEDRANGE,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.ExpectedRange)
  ))
_sym_db.RegisterMessage(ExpectedRange)

UploadStatus = _reflection.GeneratedProtocolMessageType('UploadStatus', (_message.Message,), dict(
  DESCRIPTOR = _UPLOADSTATUS,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.UploadStatus)
  ))
_sym_db.RegisterMessage(UploadStatus)

UploadedFile = _reflection.GeneratedProtocolMessageType('UploadedFile', (_message.Message,), dict(
  DESCRIPTOR = _UPLOADEDFILE,
  __module__ = 'onedrive_client.entities.onedrive_pb2'
  # @@protoc_insertion_point(class_scope:onedrive_client.entities.onedrive.UploadedFile)
  ))
_sym_db.RegisterMessage(UploadedFile)


# @@protoc_insertion_point(module_scope)
