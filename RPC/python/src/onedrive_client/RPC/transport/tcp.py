"""Provides TCP-based ``Transport`` implementation."""
import collections
import struct
import sys
from types import TracebackType
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import weakref

import gevent
import gevent.event
import gevent.lock
import gevent.queue
import gevent.select
import gevent.server
import gevent.socket
import gevent.threadpool

import logbook

from .base import Transport
from .exceptions import (
    Closed,
    TransportConnectionError,
    UnknownIdentity
)


__all__ = ['TCPTransport']

LOGGER = logbook.Logger(__name__)

Address = Tuple[str, int]  # pylint: disable=invalid-name


class TCPTransport(Transport):
    """TCP-based transport.

    Uses headers that contain message size to delimit messages.
    """
    __HEADER_SIZE = 4
    __READ_BLOCK_SIZE = 1024

    def __init__(self):
        LOGGER.trace('Instantiate TCPTransport...')
        self.__server = None
        self.__identity = None
        self.__inbound_connections = {}
        self.__on_inbound_connections_callbacks = []
        self.__on_connection_lost_callbacks = []
        self.__outbound_connections = {}
        self.__receive_buffer = collections.defaultdict(
            bytearray
        )
        self.__receive_callbacks = []
        self.__send_queue = gevent.queue.Queue()
        self.__socket_locks = weakref.WeakKeyDictionary()
        self.__closed = False

        gevent.spawn(self.__sender, weakref.ref(self), self.__send_queue)

        super().__init__()

    def __get_socket_lock(
        self,
        socket: gevent.socket.socket
    ) -> gevent.lock.RLock:
        return self.__socket_locks.setdefault(socket, gevent.lock.RLock())

    @property
    def __connections(self) -> Dict[str, gevent.socket.socket]:
        """Returns a dictionary with all the identities and
        associated sockets.
        """
        return dict(
            self.__inbound_connections,
            **self.__outbound_connections
        )

    def __reader(
        self,
        identity: str,
        socket: gevent.socket.socket
    ) -> None:
        """Tries to read and parse a message."""
        with self.__get_socket_lock(socket):
            chunk = self.__read_all(socket=socket)
            if not chunk:
                LOGGER.trace('"{}" closed connection.', identity)
                try:
                    self.disconnect(identity)
                except TransportConnectionError as exc:
                    LOGGER.exception(exc)
                    return

            buffer = self.__receive_buffer[identity]
            buffer.extend(chunk)

            while True:
                message = self.__extract_message(buffer)
                if message is not None:
                    # pylint: disable=broad-except
                    try:
                        for callback in self.__receive_callbacks:
                            callback(identity, message)
                    except Exception:
                        pass
                else:
                    break

    @staticmethod
    def __inbound_connection_handler(
        transportref: weakref.ReferenceType,
        socket: gevent.socket.socket,
        address: Address
    ) -> None:
        """Handles all inbound connections.

        Triggers externally set callbacks and reads the messages.
        """
        # pylint: disable=protected-access
        LOGGER.trace(
            'Inbound connection from "{}".',
            ':'.join(map(str, address))
        )
        transport = transportref()
        if transport is None:
            return
        identity = transport.__make_identity(address)
        transport.__inbound_connections[identity] = socket

        for callback in transport.__on_inbound_connections_callbacks:
            # pylint: disable=broad-except
            try:
                callback(identity)
            except Exception:
                pass

        watcher = gevent.spawn(
            transport.__watch_socket,
            weakref.ref(transport),
            identity,
            weakref.ref(socket)
        )
        del transport
        watcher.join()

    @staticmethod
    def __watch_socket(
        transportref: weakref.ReferenceType,
        identity: str,
        socketref: weakref.ReferenceType
    ):
        """Watches a socket for readiness to be read and triggers message
        reading and parsing.
        """
        # pylint: disable=protected-access
        while True:
            transport = transportref()
            socket = socketref()
            if (transport is None or
                transport.is_closed or
                socket is None or
                socket.fileno() == -1):
                break
            # pylint: disable=no-member
            file_ = socket.makefile()
            gevent.socket.wait_read(file_.fileno())
            transport.__reader(identity, socket)
            del transport, socket
            gevent.sleep(0.1)

    @classmethod
    def __extract_message(
        cls,
        buffer: bytearray
    ) -> Union[bytes, None]:
        """Parse message from a buffer.

        If parsing is successful - delete parsed bytes from the beginning
        of `buffer`.
        """
        if len(buffer) < cls.__HEADER_SIZE:
            return

        header = buffer[:cls.__HEADER_SIZE]
        if len(header) != cls.__HEADER_SIZE:
            return
        (body_length,) = cls.__parse_header(header)
        if (len(buffer) - cls.__HEADER_SIZE) < body_length:
            return

        body = buffer[cls.__HEADER_SIZE: cls.__HEADER_SIZE + body_length]
        del buffer[:cls.__HEADER_SIZE + body_length]

        return bytes(body)

    def __read_all(self, socket: gevent.socket.socket) -> bytes:
        """Read all available data from `socket`."""
        data = b''

        while True:
            try:
                with self.__get_socket_lock(socket):
                    current_data = socket.recv(self.__READ_BLOCK_SIZE)
            except gevent.socket.error:
                raise TransportConnectionError
            data += current_data
            if len(current_data) < self.__READ_BLOCK_SIZE:
                break
        return data

    def __close_connection(
        self,
        identity: str,
        socket: gevent.socket.socket
    ) -> None:
        LOGGER.trace(
            'Closing connection with "{}".',
            identity
        )
        self.__inbound_connections.pop(identity, None)
        self.__outbound_connections.pop(identity, None)

        try:
            with self.__get_socket_lock(socket):
                socket.shutdown(gevent.socket.SHUT_RDWR)
                socket.close()
        except gevent.socket.error as exc:
            raise TransportConnectionError(exc)

    @staticmethod
    def __make_identity(address):
        """Make an identity from `address`."""
        return ':'.join(map(str, address))

    @staticmethod
    def __make_header(data):
        """Make binary header for `data`."""
        length = len(data)
        header = struct.pack('!I', length)
        return header

    @staticmethod
    def __parse_header(header):
        """Parse `header` into components."""
        return struct.unpack('!I', header)

    @staticmethod
    def __sender(transportref, send_queue):
        """Continuously sends data.

        Notes
        -----
        The reason why sending is placed in a separate greenlet is to avoid
        problems with `thread affinity`__ of Gevent's socket objects. Otherwise
        it would be impossible to send data from another thread.

        __ https://github.com/gevent/gevent/blob/
           eef54f46d50495b2e6bc2a9b3321b3b4185eb497/doc/gevent.socket.rst
           #modgeventsocket----cooperative-low-level-networking-interface
        """
        # pylint: disable=protected-access
        transport = None
        for data, identities, sent_event in send_queue:
            del transport
            transport = transportref()
            if transport is None or transport.is_closed:
                break
            sent_to_identities = []
            for identity in identities:
                if transport.is_closed:
                    break
                socket = transport.__connections[identity]
                try:
                    with transport.__get_socket_lock(socket):
                        socket.sendall(data)
                    LOGGER.trace('Sent {} bytes to "{}".', len(data), identity)
                except gevent.socket.error as exc:
                    LOGGER.warning(exc)
                    transport.__execute_on_connection_lost_callbacks(identity)
                    try:
                        transport.__close_connection(identity, socket)
                    except TransportConnectionError:
                        pass
                sent_to_identities.append(identity)
            sent_event.set(sent_to_identities)

    def send(
        self,
        data: bytes,
        identities: Sequence[str],
        block: bool = True,
        timeout: Optional[float] = None
    ) -> Optional[List[str]]:
        """Send a message to a remote peer."""
        LOGGER.trace(
            'Sending to {}...', ', '.join('"' + i + '"' for i in identities)
        )
        if self.is_closed:
            raise Closed
        unknown_identities = set(identities) - set(self.__connections)
        if unknown_identities:
            raise UnknownIdentity(list(unknown_identities))

        header = self.__make_header(data)
        data = header + data
        sent_event = gevent.event.AsyncResult()
        self.__send_queue.put((data, identities, sent_event))
        if block:
            return sent_event.get(block=True, timeout=timeout)

    def on_receive(self, callback: Callable[[str, bytes], None]):
        """Register a 'callback' to be called when data is received.

        The 'callback' is called with two positional arguments: the sender
        identity and the data.
        """
        self.__receive_callbacks.append(callback)

    def disconnect(self, identity: str):
        """Disconnect remote peer."""
        LOGGER.debug('Disconnecting "{}"...', identity)
        if self.is_closed:
            raise Closed
        try:
            socket = self.__connections[identity]
        except KeyError:
            raise UnknownIdentity(
                'Can not disconnect "%s": the is unknown.'
            )

        try:
            with self.__get_socket_lock(socket):
                self.__close_connection(identity, socket)
        except gevent.socket.error as exc:
            raise TransportConnectionError(exc)
        finally:
            self.__execute_on_connection_lost_callbacks(identity)

    @property
    def connections(self):
        """List of inbound and outbound connection with peers."""
        return list(self.__connections.keys())

    @property
    def inbound_connections(self):
        """List of inbound connection with peers."""
        return list(self.__inbound_connections.keys())

    @property
    def outbound_connections(self):
        """List of outbound connection with peers."""
        return list(self.__outbound_connections.keys())

    @property
    def identity(self):
        """Identity associated with the instance."""
        return self.__identity

    @property
    def is_closed(self):
        """Whether the instance is is_closed."""
        return self.__closed

    def close(self):
        """Close the transport, disconnect all the peers."""
        LOGGER.trace('Closing TCPTransport instance...')
        if self.is_closed:
            raise Closed
        self.__closed = True
        self.__send_queue.put(StopIteration)
        for identity, socket in self.__connections.items():
            with self.__get_socket_lock(socket):
                self.__close_connection(identity, socket)

        if self.__server is not None:
            try:
                self.__server.stop()
            except (gevent.socket.error, OSError) as exc:
                raise TransportConnectionError(exc)

    def connect(self, address: Address) -> str:
        """Connect to a remote peer."""
        LOGGER.trace('Connecting to "{}"...', ':'.join(map(str, address)))
        if self.is_closed:
            raise Closed
        try:
            socket = gevent.socket.create_connection(
                address=address
            )
        except gevent.socket.error as exc:
            raise TransportConnectionError(exc)
        LOGGER.trace('Connected to "{}".', ':'.join(map(str, address)))

        identity = self.__make_identity(address)
        self.__outbound_connections[identity] = socket
        gevent.spawn(
            self.__watch_socket,
            weakref.ref(self),
            identity,
            weakref.ref(socket)
        )

        return identity

    def serve(self, address: Address):
        """Binds a transport-instance to an address."""
        if self.is_closed:
            raise Closed
        address_repr = ':'.join(map(str, address))
        LOGGER.debug('Listening on "{}".', address_repr)
        bound_socket = None
        server = None
        try:
            bound_socket = gevent.socket.socket()
            bound_socket.setsockopt(
                gevent.socket.SOL_SOCKET,
                gevent.socket.SO_REUSEADDR,
                1
            )
            bound_socket.bind(address)
            bound_socket.listen()
            identity = self.__make_identity(bound_socket.getsockname())
            server = gevent.server.StreamServer(
                bound_socket,
                handle=lambda *a, **kw: self.__inbound_connection_handler(
                    weakref.ref(self), *a, **kw
                )
            )
            self.__server = server
            self.__identity = identity
            server.serve_forever()
        except (gevent.socket.error, OSError) as exc:
            raise TransportConnectionError(exc)
        finally:
            LOGGER.trace('Stopped listening on "{}".', address_repr)
            self.__identity = None
            self.__server = None
            if server is not None and not server.closed:
                server.stop()
            if bound_socket is not None and bound_socket.fileno() != -1:
                bound_socket.shutdown(gevent.socket.SHUT_RDWR)
                bound_socket.close()

    def on_inbound_connection(self, callback: Callable[[str], None]):
        """Set a callback that will be executed when someone connects."""
        self.__on_inbound_connections_callbacks.append(callback)

    def __execute_on_connection_lost_callbacks(self, identity):
        exc_info = sys.exc_info()
        for callback in self.__on_connection_lost_callbacks:
            # pylint: disable=broad-except
            try:
                callback(identity, *exc_info)
            except Exception:
                pass

    def on_connection_lost(
        self,
        callback: Callable[
            [
                str,
                Optional[type],
                Optional[Exception],
                Optional[TracebackType]
            ],
            None
        ]
    ):
        """Set a callback that will be executed when a disconnect happens."""
        self.__on_connection_lost_callbacks.append(callback)
