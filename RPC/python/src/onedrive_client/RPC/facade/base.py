"""Provides ``FacadeMeta`` metaclass."""
import functools as ft
import re
import time as timelib
from typing import Callable, Optional

import logbook

# pylint: disable=no-name-in-module,import-error
from onedrive_client.entities import Entity, get_entity
from onedrive_client.RPC.peer import Peer
from onedrive_client.RPC.peer.endpoint import Endpoint


LOGGER = logbook.Logger(__name__)


class FacadeMeta(type):
    """Generates service facade-class based on the descriptor."""
    def __new__(mcs, name, bases, attributes):
        descriptor = attributes['DESCRIPTOR']

        attributes['__init__'] = mcs.__make_init()

        methods = descriptor.methods_by_name.items()
        service_options = {
            d.name: value for d, value in
            descriptor.GetOptions().ListFields()
        }
        service_id = service_options['service_id']

        for method_name, method_descriptor in methods:
            method_options = {
                d.name: value for d, value in
                method_descriptor.GetOptions().ListFields()
            }
            method_id = method_options['method_id']

            def open_session(self, service_id=service_id, method_id=method_id):
                # pylint: disable=protected-access
                return self.__peer.open_session(
                    service_id=service_id,
                    method_id=method_id
                )
            name = open_session.__name__ = (
                'open_' + mcs.__to_snake_case(method_name) + '_session'
            )
            attributes[name] = open_session

            def on_inbound_session(
                self,
                callback,
                service_id=service_id,
                method_id=method_id
            ):
                # pylint: disable=protected-access
                return self.__peer.on_inbound_session(
                    callback=callback,
                    service_id=service_id,
                    method_id=method_id
                )

            name = on_inbound_session.__name__ = (
                'on_inbound_' + mcs.__to_snake_case(method_name) + '_session'
            )
            attributes[name] = on_inbound_session

        return super().__new__(mcs, name, bases, attributes)

    @classmethod
    def __make_init(mcs):
        def __init__(
            self,
            transport,
            acknowledgement_interval=0.5,
            heartbeat_interval=5.0,
            alive_timeout=15.0,
            sender_window_size=1000,
            receiver_window_size=1000,
            time=timelib.time
        ):
            # pylint: disable=protected-access
            self.__peer = Peer(
                transport=transport,
                services=[self.DESCRIPTOR],
                endpoint_factory=facade_endpoint_factory,
                acknowledgement_interval=acknowledgement_interval,
                heartbeat_interval=heartbeat_interval,
                alive_timeout=alive_timeout,
                sender_window_size=sender_window_size,
                receiver_window_size=receiver_window_size,
                time=time
            )
        return __init__

    @staticmethod
    def __to_snake_case(string):
        string = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', string).lower()


class FacadeEndpointAdapter(Endpoint):
    """Provides facade for the ``Endpoint`` class.

    Provides conversion of the messages from Protobuf native classes to
    ``Entity`` subclasses.
    """
    # pylint: disable=missing-docstring
    def send(  # pylint: disable=arguments-differ
        self,
        message: Optional[Entity] = None,
        *args,
        **kwargs
    ):
        if message is not None:
            message = message.to_protobuf_message()

        return super().send(
            message=message,
            *args,
            **kwargs
        )

    def on_receive(self, callback: Callable[[str, Entity], None]):
        @ft.wraps(callback)
        def callback_wrapper(identity, message):
            LOGGER.trace(
                'Adapting message {}',
                message.DESCRIPTOR.full_name
            )
            entity_cls = get_entity(message.DESCRIPTOR.full_name)
            message = entity_cls.from_protobuf_message(message)
            return callback(identity, message)

        return super().on_receive(callback_wrapper)


def facade_endpoint_factory(*args, **kwargs):
    return FacadeEndpointAdapter(*args, **kwargs)
