"""Provides ``Peer`` class."""
import collections
import time as timelib
from typing import Callable, Sequence, Tuple

from google.protobuf.descriptor import ServiceDescriptor
from google.protobuf.message import DecodeError
from google.protobuf.reflection import MakeClass
import logbook

from onedrive_client.RPC.transport import Transport
from .endpoint import Endpoint
from .exceptions import PeerError, ServiceNotFound
from ..models import get_model
from ..RPC_pb2 import (
    method_id as method_id_option,
    model_id as model_id_option,
    Packet,
    service_id as service_id_option
)


LOGGER = logbook.Logger(__name__)


def default_endpoint_factory(*args, **kwargs):
    return Endpoint(*args, **kwargs)


class Peer:
    """Manages and creates endpoints and routes packets to them."""
    def __init__(
        self,
        transport: Transport,
        services: Sequence[ServiceDescriptor],
        endpoint_factory: Callable = default_endpoint_factory,
        acknowledgement_interval=0.5,
        heartbeat_interval=5.0,
        alive_timeout=15.0,
        sender_window_size=1000,
        receiver_window_size=1000,
        time=timelib.time
    ):
        self.__transport = transport
        self.__services = services
        self.__endpoints = {}
        self.__endpoint_factory = endpoint_factory
        self.__acknowledgement_interval = acknowledgement_interval
        self.__heartbeat_interval = heartbeat_interval
        self.__alive_timeout = alive_timeout
        self.__sender_window_size = sender_window_size
        self.__receiver_window_size = receiver_window_size
        self.__time = time
        self.__is_closed = False
        self.__on_inbound_session_callbacks = collections.defaultdict(list)

        self.__transport.on_receive(self.__on_receive)

    def __on_receive(self, identity, data):
        # pylint: disable=no-member,broad-except
        LOGGER.trace('Received {} bytes from {}...', len(data), identity)
        if self.is_closed:
            LOGGER.trace('Peer is closed. Doing nothing')
            return
        packet = Packet()
        try:
            packet.ParseFromString(data)
        except (DecodeError, TypeError) as exc:
            LOGGER.exception(exc)
            return

        LOGGER.trace('Received packet #{}...', packet.packet_id)
        LOGGER.trace(
            'Session ID: {}',
            repr(packet.session_id.value
                 if packet.HasField('session_id')
                 else None)
        )
        try:
            endpoint, is_new = self.__open_session(
                packet.service_id,
                packet.method_id,
                (packet.session_id.value
                 if packet.HasField('session_id')
                 else None)
            )
        except ServiceNotFound as exc:
            LOGGER.exception(exc)
            LOGGER.trace(
                'Service ID: {}, Method ID: {}',
                packet.service_id,
                packet.method_id
            )
            return

        if endpoint.is_closed:
            LOGGER.trace('Endpoint is closed. Skipping...')
            return

        if is_new:
            i = 0
            for i, callback in enumerate(
                self.__on_inbound_session_callbacks.get(
                    (packet.service_id, packet.method_id),
                    []
                ),
                start=1
            ):
                try:
                    callback(
                        identity,
                        endpoint
                    )
                except Exception as exc:
                    LOGGER.exception(exc)
            LOGGER.trace(
                'New endpoint was created. '
                'Session: {}. '
                'Callbacks executed: {}.',
                repr(endpoint.session_id),
                i
            )

        try:
            LOGGER.trace('Feeding the packet to the endpoint...')
            endpoint.consume_packet(identity, packet)
        except PeerError as exc:
            LOGGER.exception(exc)

    def __get_method(self, service_id, method_id):
        service_descriptor = next(
            (s for s in self.__services
             if s.GetOptions().Extensions[service_id_option] == service_id),
            None
        )
        if service_descriptor is None:
            return None

        method_descriptor = next(
            (s for s in service_descriptor.methods
             if s.GetOptions().Extensions[method_id_option] == method_id),
            None
        )

        if method_descriptor is None:
            return None

        model_id = method_descriptor.GetOptions().Extensions[model_id_option]
        model_cls = get_model(model_id)

        if model_cls is None:
            return None

        request_cls = MakeClass(method_descriptor.input_type)
        response_cls = MakeClass(method_descriptor.output_type)

        return (
            service_descriptor,
            method_descriptor,
            model_cls,
            request_cls,
            response_cls
        )

    def __open_session(
        self,
        service_id: int,
        method_id: int,
        session_id: int = None
    ) -> Tuple[Endpoint, bool]:
        """Open new endpoint."""
        is_new = False
        method = self.__get_method(service_id, method_id)
        if method is None:
            raise ServiceNotFound

        (_,
         _,
         model_cls,
         request_cls,
         _) = method

        endpoint = None
        if model_cls.SINGLETON_SESSION:
            endpoint = self.__endpoints.get((service_id, method_id, None))
        elif session_id is not None:
            endpoint = self.__endpoints.get(
                (service_id, method_id, session_id)
            )

        if endpoint is not None:
            return endpoint, is_new

        model = model_cls()
        endpoint = self.__endpoint_factory(
            service_id=service_id,
            method_id=method_id,
            model=model,
            session_id=session_id,
            message_cls=request_cls,
            acknowledgement_interval=self.__acknowledgement_interval,
            heartbeat_interval=self.__heartbeat_interval,
            alive_timeout=self.__alive_timeout,
            send=lambda data, identities: self.__transport.send(
                data=data,
                identities=identities
            ),
            sender_window_size=self.__sender_window_size,
            receiver_window_size=self.__receiver_window_size,
            time=self.__time
        )
        is_new = True
        if model_cls.SINGLETON_SESSION:
            self.__endpoints[(service_id, method_id, None)] = endpoint
        else:
            self.__endpoints[
                (service_id, method_id, endpoint.session_id)
            ] = endpoint

        return endpoint, is_new

    def open_session(self, service_id, method_id):
        """Create an endpoint for a new session."""
        endpoint, _ = self.__open_session(
            service_id=service_id,
            method_id=method_id
        )
        return endpoint

    def on_inbound_session(
        self,
        callback: Callable[[str, Endpoint, int, int], None],
        service_id,
        method_id
    ):
        """Subscribe the 'callback' to be called on new inbound session."""
        self.__on_inbound_session_callbacks[(service_id, method_id)].append(
            callback
        )

    def connect(self, address) -> str:
        return self.__transport.connect(address=address)

    def disconnect(self, identity: str):
        return self.__transport.disconnect(identity=identity)

    def serve(self, address):
        return self.__transport.serve(address)

    @property
    def is_closed(self):
        return self.__is_closed

    def close(self, force=False):
        """Close peer."""
        for endpoint in self.__endpoints.values():
            endpoint.close(force=force)
        self.__transport.close()
        self.__is_closed = True
