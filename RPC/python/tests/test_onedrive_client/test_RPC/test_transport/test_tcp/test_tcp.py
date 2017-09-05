"""Tests of ``TCPTransport``."""
import socket
from typing import Tuple
from unittest import mock

import gevent
import psutil
import pytest

from onedrive_client.RPC.transport import TCPTransport, UnknownIdentity

from tests.utils.gevent import wait_until


class TestTCPTransport:
    """Tests for ``TCPTransport`` class."""
    # pylint: disable=redefined-outer-name,
    @staticmethod
    def test_one_way_message(
        tcp_transport: TCPTransport,
        tcp_transport_b: TCPTransport,
        connection_b: Tuple[str, str],
        timeout: float
    ):
        """Simple sending of a message in one direction."""
        expected_message = b'test_message'
        identity, identity_b = connection_b

        actual_from_identity, actual_message = None, None

        def callback(identity, data):
            nonlocal actual_from_identity, actual_message
            actual_from_identity = identity
            actual_message = data

        tcp_transport.on_receive(callback)
        tcp_transport_b.send(expected_message, [identity])

        wait_until(
            lambda: (actual_from_identity, actual_message) != (None, None),
            timeout=timeout
        )
        assert actual_from_identity == identity_b
        assert actual_message == expected_message

    @staticmethod
    def test_simple_exchange(
        tcp_transport: TCPTransport,
        tcp_transport_b: TCPTransport,
        connection_b: Tuple[str, str],
        timeout: float
    ):
        """Message exchange between two peers."""
        expected_message = b'test_message'
        expected_message_b = b'test_message_b'
        identity, identity_b = connection_b

        actual_from_identity, actual_message = None, None

        def callback(identity, data):
            nonlocal actual_from_identity, actual_message
            actual_from_identity = identity
            actual_message = data

        tcp_transport.on_receive(callback)
        tcp_transport_b.send(expected_message, [identity])

        wait_until(
            lambda: (actual_from_identity, actual_message) != (None, None),
            timeout=timeout
        )
        assert actual_from_identity == identity_b
        assert actual_message == expected_message

        tcp_transport_b.on_receive(callback)
        tcp_transport.send(expected_message_b, [identity_b])

        wait_until(
            lambda: (actual_from_identity, actual_message) != (None, None),
            timeout=timeout
        )
        assert actual_from_identity == identity
        assert actual_message == expected_message_b

    @staticmethod
    def test_receive_from_multiple_peers(
        bound_tcp_transport: TCPTransport,
        connection_b: Tuple[str, str],
        connection_c: Tuple[str, str],
        tcp_transport_b: TCPTransport,
        tcp_transport_c: TCPTransport,
        timeout: float
    ):
        """Messages sent from multiple peers are received."""
        expected_message_1 = b'test_message'
        expected_message_2 = b'test_message_b'

        messages = []

        def callback(_, data):
            messages.append(data)

        bound_tcp_transport.on_receive(callback)

        tcp_transport_b.send(expected_message_1, [connection_b[0]])
        tcp_transport_c.send(expected_message_2, [connection_c[0]])

        wait_until(lambda: len(messages) >= 2, timeout=timeout)

        assert expected_message_1 in messages
        assert expected_message_2 in messages

    @staticmethod
    def test_send_to_multiple_peers(
        bound_tcp_transport: TCPTransport,
        connection_b: Tuple[str, str],
        connection_c: Tuple[str, str],
        tcp_transport_b: TCPTransport,
        tcp_transport_c: TCPTransport,
        timeout: float
    ):
        """Messages sent from multiple peers are received."""
        expected_message_b = b'test_message_b'
        expected_message_c = b'test_message_c'

        messages_b = []

        def callback_b(_, data):
            messages_b.append(data)

        messages_c = []

        def callback_c(_, data):
            messages_c.append(data)

        tcp_transport_b.on_receive(callback_b)
        tcp_transport_c.on_receive(callback_c)

        bound_tcp_transport.send(expected_message_b, [connection_b[1]])
        bound_tcp_transport.send(expected_message_c, [connection_c[1]])

        assert wait_until(
            lambda: len(messages_b) >= 1 and len(messages_c) >= 1,
            timeout=timeout
        )

        assert messages_b == [expected_message_b]
        assert messages_c == [expected_message_c]

    @staticmethod
    def test_serve_binds_socket(
        tcp_transport: TCPTransport,
        local_address: Tuple[str, int],
        timeout
    ):
        """serve() method binds a TCP socket."""
        gevent.spawn(tcp_transport.serve, local_address)

        assert wait_until(
            lambda: next((
                True for c in psutil.net_connections()
                if (c.family == socket.AF_INET and
                    c.type == socket.SOCK_STREAM and
                    c.status == psutil.CONN_LISTEN and
                    c.laddr == local_address)),
                False),
            timeout=timeout
        )

    @staticmethod
    def test_close_stops_server(
        local_address: Tuple[str, int],
        timeout: float
    ):
        """close() method stops the server launched by method serve()."""
        tcp_transport = TCPTransport()
        serve_greenlet = gevent.spawn(tcp_transport.serve, local_address)

        wait_until(lambda: tcp_transport.identity is not None)

        tcp_transport.close()
        assert tcp_transport.is_closed

        serve_greenlet.join(timeout=timeout)
        assert serve_greenlet.successful()

    @staticmethod
    def test_disconnect(
        bound_tcp_transport: TCPTransport,
        tcp_transport_b: TCPTransport,
        connection_b: Tuple[str, str],
        timeout: float
    ):
        """disconnect() method disconnects peer."""
        assert len(bound_tcp_transport.connections) == 1
        assert len(bound_tcp_transport.inbound_connections) == 1

        tcp_transport_b.disconnect(connection_b[0])

        wait_until(
            lambda: len(bound_tcp_transport.connections) == 0,
            timeout=timeout
        )

        assert not bound_tcp_transport.connections
        assert not bound_tcp_transport.inbound_connections

        with pytest.raises(UnknownIdentity):
            tcp_transport_b.send(b'test_data', [connection_b[0]])

        with pytest.raises(UnknownIdentity):
            bound_tcp_transport.send(b'test_data', [connection_b[1]])

    @staticmethod
    def test_on_connection_lost(
        bound_tcp_transport: TCPTransport,
        tcp_transport_b: TCPTransport,
        connection_b: Tuple[str, str],
        timeout: float
    ):
        """on_connection_lost() allows to subscribe a callback that would be
        fired when a peer disconnects.
        """
        actual_identity = None

        def callback(identity, *_):
            nonlocal actual_identity
            actual_identity = identity

        bound_tcp_transport.on_connection_lost(callback)
        tcp_transport_b.disconnect(connection_b[0])

        assert wait_until(
            lambda: not bound_tcp_transport.connections,
            timeout=timeout
        )

        assert actual_identity == connection_b[1]

    @pytest.fixture
    @staticmethod
    def make_tcp_transport(request):
        """Factory that makes ``TCPTransport`` instances.

        It also closes them on teardown.
        """
        transports = []

        def _make_tcp_transport():
            transport = TCPTransport()
            transports.append(transport)
            return transport

        def finalizer():
            for transport in transports:
                transport.close()

        request.addfinalizer(finalizer)

        _make_tcp_transport.__name__ = 'make_tcp_transport'
        return _make_tcp_transport

    @pytest.fixture
    @staticmethod
    def tcp_transport(make_tcp_transport):
        """``TCPTransport`` instance."""
        return make_tcp_transport()

    @pytest.fixture
    @staticmethod
    def tcp_transport_b(make_tcp_transport):
        """Second ``TCPTransport`` instance."""
        return make_tcp_transport()

    @pytest.fixture
    @staticmethod
    def tcp_transport_c(make_tcp_transport):
        """Second ``TCPTransport`` instance."""
        return make_tcp_transport()

    @pytest.fixture()
    @staticmethod
    def bound_tcp_transport(tcp_transport, local_address):
        """``TCPTransport`` instance bound to ``local_address``."""
        gevent.spawn(tcp_transport.serve, local_address)
        return tcp_transport

    @pytest.fixture()
    @staticmethod
    def add_connection(bound_tcp_transport, timeout, local_address):
        """Factory that adds a connection to 'bound_tcp_transport'."""
        def _add_connection(transport):
            new_identity = None

            def on_inbound_connection(identity):
                nonlocal new_identity
                new_identity = identity

            on_inbound_connection = mock.Mock(wraps=on_inbound_connection)
            bound_tcp_transport.on_inbound_connection(on_inbound_connection)

            identity = transport.connect(local_address)
            wait_until(lambda: new_identity is not None, timeout=timeout)

            on_inbound_connection.assert_called_once()
            assert identity is not None
            assert new_identity is not None

            return identity, new_identity
        _add_connection.__name__ = 'add_connection'
        return _add_connection

    @pytest.fixture()
    @staticmethod
    def connection_b(
        tcp_transport_b,
        add_connection,
    ):
        """Setup b connection between``tcp_transport`` and
        ``tcp_transport_b``.
        """
        return add_connection(tcp_transport_b)

    @pytest.fixture()
    @staticmethod
    def connection_c(
        tcp_transport_c,
        add_connection,
    ):
        """Setup b connection between``tcp_transport`` and
        ``tcp_transport_c``.
        """
        return add_connection(tcp_transport_c)
