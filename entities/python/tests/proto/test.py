"""AUTO-GENERATED WITH PROTOCOL BUFFERS COMPILER. DO NOT EDIT BY HAND.

For descriptions and comments refer to:

    tests/proto/test.proto
"""
import enum

from onedrive_client.entities import Entity

from . import test_pb2
# noqa: D101
# pylint: disable=abstract-method


# Messages
class Bar(Entity):  # noqa: D101
    _DESCRIPTOR = test_pb2.Bar.DESCRIPTOR


class Foo(Entity):  # noqa: D101
    _DESCRIPTOR = test_pb2.Foo.DESCRIPTOR


# Enums
class CarManufacturer(enum.IntEnum):  # noqa: D101
    AUDI = 0
    MERCEDES = 1
    TOYOTA = 2
