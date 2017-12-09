"""Provides ``LocalMemoryTransport`` class."""
import enum
import itertools as it
import random as rnd
from typing import Callable, Dict, Tuple
import uuid
import weakref

import gevent.lock
import gevent.queue
import logbook

from onedrive_client.RPC.transport import Transport
from onedrive_client.RPC.transport import UnknownIdentity


LOGGER = logbook.Logger(__name__)


Address = Tuple[str]  # pylint: disable=invalid-name


class Flag(enum.Enum):
    Initial = 'INITIAL'
    Close = 'INITIAL'


class LocalMemoryTransport(Transport):
    """Transport implementation that uses local memory.

    Useful for tests.
    """
    def __init__(self, packets: Dict[str, gevent.queue.Queue]):
        # pylint: disable=super-init-not-called
        self.__packets = packets
        self.__active_inbound_connections = {}
        self.__active_outbound_connections = {}
        self.__identity = None
        self.__address = None
        self.__is_closed = False
        self.__server_greenlet = False
        self.__on_inbound_connections_callbacks = []
        self.__on_receive_callbacks = []
        self.__on_connection_lost_callbacks = []
        self.__lock = gevent.lock.RLock()
        self.__connection_watcher_greenlet = gevent.spawn(
            self.__connection_watcher,
            weakref.ref(self)
        )

    def __call_on_connection_lost_callbacks(self, identity):
        for callback in self.__on_connection_lost_callbacks:
            # pylint: disable=broad-except
            try:
                callback(identity)
            except Exception as exc:
                LOGGER.exception(exc)

    def __close_outbound_connection(self, identity):
        self.__active_outbound_connections.pop(identity, None)
        self.__call_on_connection_lost_callbacks(identity)

    def __close_inbound_connection(self, identity):
        self.__active_inbound_connections.pop(identity, None)
        self.__call_on_connection_lost_callbacks(identity)

    @staticmethod
    def __server(transportref):
        # pylint: disable=protected-access
        while True:
            gevent.sleep(0.001)
            transport = transportref()
            if transport is None:
                break
            if transport.__is_closed:
                break

            host_identity = transport.__identity
            if host_identity is None:
                break

            with transport.__lock:
                try:
                    data, client_identity = (
                        transport
                            .__packets
                            .setdefault(
                                transport.__identity,
                                gevent.queue.Queue()
                            )
                            .get(timeout=0.001)
                    )
                except gevent.queue.Empty:
                    continue

                if (data is Flag.Initial and
                    client_identity not in
                    transport.__active_inbound_connections):
                    transport.__active_inbound_connections[
                        client_identity
                    ] = host_identity
                    LOGGER.trace(
                        'Incoming connection from {}.',
                        client_identity
                    )
                    callbacks = transport.__on_inbound_connections_callbacks
                    for callback in callbacks:
                        # pylint: disable=broad-except
                        try:
                            callback(client_identity)
                        except Exception as exc:
                            LOGGER.exception(exc)
                            continue

    @staticmethod
    def __connection_watcher(transportref):
        # pylint: disable=protected-access
        while True:
            gevent.sleep(0.001)
            transport = transportref()
            if transport is None:
                break
            if transport.__is_closed:
                break

            host_identities = list(it.chain(
                transport.__active_inbound_connections.values(),
                transport.__active_outbound_connections.values()
            ))
            if not host_identities:
                continue

            host_identity = rnd.choice(host_identities)

            with transport.__lock:
                try:
                    data, client_identity = (
                        transport
                            .__packets
                            .setdefault(
                                host_identity,
                                gevent.queue.Queue()
                            )
                            .get(timeout=0.001)
                    )
                except gevent.queue.Empty:
                    continue

                if data is Flag.Initial or data is Flag.Close:
                    LOGGER.trace(
                        'Received flag {} from {}.',
                        data.name,
                        client_identity
                    )
                    if (data is Flag.Close and
                        client_identity in
                        transport.__active_outbound_connections):
                        transport.__close_outbound_connection(client_identity)
                    elif (data is Flag.Close and
                          client_identity
                          in transport.__active_inbound_connections):
                        transport.__close_inbound_connection(client_identity)

                    continue
                LOGGER.trace(
                    'Received {} bytes from {}',
                    len(data),
                    client_identity
                )

                for callback in transport.__on_receive_callbacks:
                    # pylint: disable=broad-except
                    try:
                        callback(client_identity, data)
                    except Exception as exc:
                        LOGGER.exception(exc)

    def serve(self, address: Address) -> None:
        """Binds a transport-instance to an address."""
        self.__address  = address
        self.__identity = self.__make_identity(address)
        self.__server_greenlet = gevent.spawn(self.__server(weakref.ref(self)))
        return gevent.wait(self.__server_greenlet)

    def on_inbound_connection(self, callback):
        """Set a callback that will be executed when someone connects."""
        self.__on_inbound_connections_callbacks.append(callback)

    @property
    def inbound_connections(self):
        """List of inbound connection with peers."""
        return list(self.__active_inbound_connections)

    @property
    def identity(self):
        """Identity associated with the instance."""
        return self.__identity

    @staticmethod
    def __make_identity(address):
        return f'id_{address}'

    def connect(self, address: Address):
        """Connect to a remote peer."""
        client_address = str(uuid.uuid4())
        client_identity = self.__make_identity(client_address)
        host_identity = self.__make_identity(address)
        self.__send_data(
            Flag.Initial,
            client_identity,
            host_identity
        )
        self.__active_outbound_connections[host_identity] = client_identity
        return host_identity

    def disconnect(self, identity):
        """Disconnect remote peer."""
        with self.__lock:
            if identity in self.__active_outbound_connections:
                connections = self.__active_outbound_connections
            elif identity in self.__active_inbound_connections:
                connections = self.__active_inbound_connections
            else:
                raise UnknownIdentity(identity)

            del connections[identity]

    def on_connection_lost(self, callback):
        """Set a callback that will be executed when a disconnect happens.

        If a disconnect happened because of an exception - information about
        the exception is passed as three optional arguments that are the
        same as the info returned by ``sys.exc_info()``.
        """
        self.__on_connection_lost_callbacks.append(callback)

    @property
    def outbound_connections(self):
        """List of outbound connection with peers."""
        return list(self.__active_outbound_connections)

    def __send_data(self, data, from_identity, to_identity):
        (self.__packets
            .setdefault(to_identity, gevent.queue.Queue())
            .put((data, from_identity)))

    def close(self) -> None:
        """Close the transport, disconnect all the peers."""
        with self.__lock:
            self.__address = None
            self.__is_closed = True
            for client_address, host_address in list(
                self.__active_inbound_connections.items()
            ):
                self.__send_data(Flag.Close, client_address, host_address)
                self.__close_inbound_connection(client_address)
            for client_address, host_address in list(
                self.__active_outbound_connections.items()
            ):
                self.__send_data(Flag.Close, client_address, host_address)
                self.__close_outbound_connection(client_address)

        gevent.wait(self.__server_greenlet)

    @property
    def is_closed(self) -> bool:
        """Whether the instance is is_closed."""
        return self.__is_closed

    def send(
        self,
        data,
        identities,
        block=True,
        timeout=None
    ):
        """Send a message to a remote peer.

        If some of the peers identified by 'identities' are disconnected,
        they must be skipped.

        The identities to which sending was successful must be returned in
        case if 'block' is ``True``.
        """
        LOGGER.trace('Sending data to {}', ', '.join(identities))
        with self.__lock:
            unknown_identities = (
                set(identities) -
                set(self.__active_outbound_connections) -
                set(self.__active_inbound_connections)
            )
            if unknown_identities:
                raise UnknownIdentity(unknown_identities)

            for to_identity in identities:
                from_identity = self.__active_outbound_connections.get(
                    to_identity
                )
                if from_identity is None:
                    from_identity = self.__active_inbound_connections.get(
                        to_identity
                    )

                self.__send_data(data, from_identity, to_identity)
        return identities

    def on_receive(
        self,
        callback: Callable[[str, bytes], None]
    ):
        """Register a 'callback' to be called when data is received.

        The 'callback' is called with two positional arguments: the sender
        identity and the data.
        """
        self.__on_receive_callbacks.append(callback)
