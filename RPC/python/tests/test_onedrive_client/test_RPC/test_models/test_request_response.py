"""Integration tests for the Request-Response communication model."""
from unittest.mock import Mock

import gevent
import logbook

from tests.entities import Foo
from tests.service import SpamService
from tests.utils.gevent import wait_until
from tests.utils.local_memory_transport import LocalMemoryTransport
# pylint: disable=no-self-use


LOGGER = logbook.Logger(__name__)


class TestRequestResponse:
    """Integration tests for the Request-Response communication model."""
    # pylint: disable=no-member
    def test_simple_exchange(self, timeout):
        """Generic sanity check for overall model validity.

        The scenario is that the client sends requests and awaits for response.
        Server in turn awaits for request and sends the response. At the end
        the session is supposed to be closed.
        """
        # pylint: disable=missing-docstring
        packets = {}

        # Instantiate transports
        client_transport = LocalMemoryTransport(packets)
        server_transport = LocalMemoryTransport(packets)

        # Start the server
        server_address = 'server_address'
        gevent.spawn(server_transport.serve, server_address)

        # Connect to the server
        server_identity = client_transport.connect(server_address)

        # Instantiate the client and the server services
        client_service = SpamService(transport=client_transport)
        server_service = SpamService(transport=server_transport)

        expected_response = Foo(data='response')

        # Setup server handler

        server_endpoint = None
        actual_request = None

        def handle_inbound_session(identity, endpoint):
            nonlocal server_endpoint
            if server_endpoint is None:
                server_endpoint = endpoint

            LOGGER.debug(
                'Inbound new session from {}',
                identity
            )

            def handle_request(from_identity, message):
                nonlocal actual_request
                actual_request = message
                LOGGER.debug(
                    'Request from {}: \n{}',
                    from_identity,
                    repr(message)
                )
                LOGGER.debug(
                    'Sending response to {}',
                    from_identity
                )
                endpoint.send(
                    message=expected_response,
                    identity=from_identity
                )

            endpoint.on_receive(handle_request)

        server_service.on_inbound_bar_session(handle_inbound_session)

        # Open new client session.
        client_endpoint = client_service.open_bar_session()

        # Setup response handler.
        actual_from_identity, actual_response = None, None

        def on_receive(from_identity, message):
            nonlocal actual_from_identity, actual_response
            actual_from_identity = from_identity
            actual_response = message

        client_endpoint.on_receive(on_receive)

        # Send request.
        expected_request = request = Foo(data='request')
        client_endpoint.send(
            message=request,
            identity=server_identity
        )

        wait_until(lambda: actual_request is not None, timeout=timeout)
        assert actual_request == expected_request

        assert wait_until(
            lambda: server_endpoint is not None,
            timeout=timeout
        )
        assert wait_until(
            lambda: actual_from_identity is not None,
            timeout=timeout
        )
        assert wait_until(
            lambda: actual_response is not None,
            timeout=timeout
        )

        assert actual_from_identity == server_identity
        assert actual_response == expected_response

        assert wait_until(lambda: server_endpoint.is_closed, timeout=timeout)
        assert wait_until(lambda: client_endpoint.is_closed, timeout=timeout)

    def test_premature_close_by_server(self, timeout):
        """Tests situation when the server abruptly closes the session.

        When the server sends a close request before returning a response
        - session must be closed on both of the ends.
        """
        # pylint: disable=missing-docstring
        packets = {}
        client_transport = LocalMemoryTransport(packets)
        server_transport = LocalMemoryTransport(packets)

        server_address = 'server_address'
        gevent.spawn(server_transport.serve, server_address)
        server_identity = client_transport.connect(server_address)

        client_service = SpamService(transport=client_transport)
        server_service = SpamService(transport=server_transport)

        server_endpoint = None
        actual_request = None

        def handle_inbound_session(identity, endpoint):
            nonlocal server_endpoint
            if server_endpoint is None:
                server_endpoint = endpoint

            LOGGER.debug(
                'Inbound new session from {}',
                identity
            )

            def handle_request(from_identity, message):
                nonlocal actual_request
                actual_request = message
                LOGGER.debug(
                    'Request from {}: \n{}',
                    from_identity,
                    repr(message)
                )
                LOGGER.debug(
                    'Sending response to {}',
                    from_identity
                )
                endpoint.send(
                    identity=from_identity,
                    is_close=True
                )

            endpoint.on_receive(handle_request)

        server_service.on_inbound_bar_session(handle_inbound_session)

        # Open new session.
        client_endpoint = client_service.open_bar_session()

        def _on_receive(*_, **__):
            pass

        on_receive = Mock(wraps=_on_receive)

        client_endpoint.on_receive(on_receive)

        expected_request = request = Foo(data='request')
        client_endpoint.send(
            message=request,
            identity=server_identity
        )

        wait_until(lambda: actual_request is not None, timeout=timeout)
        assert actual_request == expected_request

        assert wait_until(
            lambda: server_endpoint is not None,
            timeout=timeout
        )
        assert wait_until(lambda: server_endpoint.is_closed, timeout=timeout)
        assert wait_until(lambda: client_endpoint.is_closed, timeout=timeout)
        assert on_receive.call_count == 0

    def test_premature_close_by_client(self, timeout):
        """Tests situation when the client abruptly closes the session.

        When the client sends a close request before receiving a response
        - session must be closed on both of the ends.
        """
        # pylint: disable=missing-docstring
        packets = {}
        client_transport = LocalMemoryTransport(packets)
        server_transport = LocalMemoryTransport(packets)

        server_address = 'server_address'
        gevent.spawn(server_transport.serve, server_address)
        server_identity = client_transport.connect(server_address)

        client_service = SpamService(transport=client_transport)
        server_service = SpamService(transport=server_transport)

        server_endpoint = None
        actual_request = None
        server_handler_call_count = 0

        def handle_inbound_session(identity, endpoint):
            nonlocal server_endpoint
            if server_endpoint is None:
                server_endpoint = endpoint

            LOGGER.debug(
                'Inbound new session from {}',
                identity
            )

            def handle_request(from_identity, message):
                nonlocal actual_request, server_handler_call_count
                server_handler_call_count += 1
                actual_request = message
                LOGGER.debug(
                    'Request from {}: \n{}',
                    from_identity,
                    repr(message)
                )
                LOGGER.debug(
                    'Sending response to {}',
                    from_identity
                )

            endpoint.on_receive(handle_request)

        server_service.on_inbound_bar_session(handle_inbound_session)

        # Open new session.
        client_endpoint = client_service.open_bar_session()

        # Setup response handler.
        def _on_receive(*_, **__):
            pass

        on_receive = Mock(wraps=_on_receive)

        client_endpoint.on_receive(on_receive)

        # Send request.
        expected_request = request = Foo(data='request')
        client_endpoint.send(
            message=request,
            identity=server_identity
        )

        assert wait_until(
            lambda: server_endpoint is not None,
            timeout=timeout
        )
        wait_until(lambda: actual_request is not None, timeout=timeout)
        assert actual_request == expected_request

        client_endpoint.send(
            is_close=True,
            identity=server_identity
        )

        assert wait_until(lambda: server_endpoint.is_closed, timeout=timeout)
        assert wait_until(lambda: client_endpoint.is_closed, timeout=timeout)
        assert on_receive.call_count == 0
