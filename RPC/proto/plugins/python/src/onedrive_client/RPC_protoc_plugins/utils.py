import sys

import logbook

from . import plugin_pb2


class Entrypoint:
    """Generic plugin entrypoint."""
    def __init__(self, generator):
        self.generator = generator

    def __call__(self):
        with logbook.StderrHandler().applicationbound():
            # Read request message from stdin
            data = sys.stdin.buffer.read()

            # Parse request
            request = plugin_pb2.CodeGeneratorRequest()
            request.ParseFromString(data)

            # Create response
            response = plugin_pb2.CodeGeneratorResponse()

            # Generate code
            self.generator(request, response)

            # Serialise response message
            output = response.SerializeToString()

            # Write to stdout
            sys.stdout.buffer.write(output)
