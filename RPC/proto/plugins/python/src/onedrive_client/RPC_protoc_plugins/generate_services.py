#!/usr/bin/env python
"""Protobuf plugin that generates DTO objects and related enums.

Refer to this page for information about Protobuf plugins:

    https://developers.google.com/protocol-buffers/docs/reference/other#plugins
"""
import re
from os import path

from .utils import Entrypoint
import logbook
import mako.template
import mako.exceptions


LOGGER = logbook.Logger('RPC_services')


TEMPLATES_PATH = path.join(path.dirname(path.abspath(__file__)), 'templates')

SERVICE_TEMPLATE = mako.template.Template(
    filename=path.join(TEMPLATES_PATH, 'service.mako')
)


def _generate_services(request, response):
    for file_descriptor in request.proto_file:
        LOGGER.info('Processing "{}".', file_descriptor.name)
        if file_descriptor.name not in request.file_to_generate:
            LOGGER.info(
                'File "{}" is not supposed to be processed, skipping.',
                file_descriptor.name
            )
            continue

        target_dir = path.dirname(path.normpath(
            file_descriptor.name
        ))
        filename, _ = path.splitext(path.basename(file_descriptor.name))

        pb_module = filename + '_pb2'
        try:
            content = SERVICE_TEMPLATE.render(
                PB_MODULE=pb_module,
                FILE_DESCRIPTOR=file_descriptor
            )
        except:
            LOGGER.error(
                mako.exceptions.text_error_template().render()
            )
            raise

        target_path = path.join(target_dir, filename + '.py')

        output_file = response.file.add()
        output_file.name = target_path
        output_file.content = content

        LOGGER.info('Writing file "{}".', target_path)


main = Entrypoint(_generate_services)
