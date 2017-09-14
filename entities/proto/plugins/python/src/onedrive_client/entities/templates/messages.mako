"""AUTO-GENERATED WITH PROTOCOL BUFFERS COMPILER. DO NOT EDIT BY HAND.

For descriptions and comments refer to:

    ${FILE_DESCRIPTOR.name}
"""
<%!
    from os import path
%>\
% if len(FILE_DESCRIPTOR.enum_type) > 0:
import enum

% endif
% if len(FILE_DESCRIPTOR.message_type) > 0:
from onedrive_client.entities import Entity

from . import ${PB_MODULE}
% endif
# noqa: D101
# pylint: disable=abstract-method


# Messages
% for message_descriptor in FILE_DESCRIPTOR.message_type:
% if not loop.first:


% endif
class ${message_descriptor.name}(Entity):  # noqa: D101
    _DESCRIPTOR = ${PB_MODULE}.${message_descriptor.name}.DESCRIPTOR
% endfor


# Enums
% for enum_descriptor in FILE_DESCRIPTOR.enum_type:
% if not loop.first:


% endif
class ${enum_descriptor.name}(enum.IntEnum):  # noqa: D101
    % for enum_value_descriptor in enum_descriptor.value:
    ${enum_value_descriptor.name} = ${enum_value_descriptor.number}
    % endfor
% endfor
