"""AUTO-GENERATED WITH PROTOCOL BUFFERS COMPILER. DO NOT EDIT BY HAND.

For descriptions and comments refer to:

${FILE_DESCRIPTOR.name}
"""
from onedrive_client.entities import *  # noqa
from onedrive_client.RPC.facade import FacadeMeta

from . import ${PB_MODULE}


% for service_descriptor in FILE_DESCRIPTOR.service:
class ${service_descriptor.name}(metaclass=FacadeMeta):
    DESCRIPTOR = ${PB_MODULE}.${service_descriptor.name}.DESCRIPTOR
% endfor
