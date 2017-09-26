"""AUTO-GENERATED WITH PROTOCOL BUFFERS COMPILER. DO NOT EDIT BY HAND.

For descriptions and comments refer to:

    onedrive_client/entities/onedrive.proto
"""
import enum

from onedrive_client.entities import Entity

from . import onedrive_pb2
# noqa: D101
# pylint: disable=abstract-method


# Messages
class BaseItem(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.BaseItem.DESCRIPTOR


class Drive(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.Drive.DESCRIPTOR


class FolderFacet(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.FolderFacet.DESCRIPTOR


class PackageFacet(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.PackageFacet.DESCRIPTOR


class DeletedFacet(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.DeletedFacet.DESCRIPTOR


class HashesFacet(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.HashesFacet.DESCRIPTOR


class FileFacet(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.FileFacet.DESCRIPTOR


class Item(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.Item.DESCRIPTOR


class ExpectedRange(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.ExpectedRange.DESCRIPTOR


class UploadStatus(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.UploadStatus.DESCRIPTOR


class UploadedFile(Entity):  # noqa: D101
    _DESCRIPTOR = onedrive_pb2.UploadedFile.DESCRIPTOR


# Enums
class DriveType(enum.IntEnum):  # noqa: D101
    PERSONAL = 0
    BUSINESS = 1
    DOCUMENT_LIBRARY = 2


class ConflictBehavior(enum.IntEnum):  # noqa: D101
    RENAME = 0
    REPLACE = 1
    FAIL = 2
