"""Tests for ``onedrive_client.RPC.peer.endpoint`` module."""
import enum
import time as timelib
from unittest.mock import Mock

import pytest

from onedrive_client.RPC.models import Action, Model
from onedrive_client.RPC.peer.endpoint import Endpoint
from onedrive_client.RPC.RPC_pb2 import Packet
from tests.entities_pb2 import Foo
from tests.utils.gevent import wait_until
# pylint: disable=too-many-public-methods


class TestEndpoint:
    """Tests for ``Endpoint`` class."""
    # pylint: disable=no-self-use,invalid-name,no-member
    def test_send_message(self, SimpleModel, make_endpoint, timeout):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        sent_data = []

        def send(data, identities):
            """Send-callback stub that appends send packet to the list."""
            nonlocal sent_data
            packet = Packet()
            packet.ParseFromString(data)
            sent_data.append((packet, identities))
            return identities

        expected_service_id = 1
        expected_method_id = 1

        endpoint: Endpoint = make_endpoint(
            service_id=expected_service_id,
            method_id=expected_method_id,
            message_cls=Foo,
            send=send,
            model=SimpleModel()
        )

        request = Foo()
        expected_data = request.data = 'test_data'
        expected_to_identity = to_identity = 'to_identity'
        endpoint.send(message=request, identity=to_identity)

        assert wait_until(
            lambda: len([1 for p, _ in sent_data if not p.is_heartbeat]) > 0,
            timeout=timeout
        )

        assert len(sent_data) == 1
        actual_packet, actual_to_identities = sent_data[0]

        assert actual_to_identities == [expected_to_identity]

        assert actual_packet.is_initial
        assert not actual_packet.is_closing
        assert not actual_packet.is_error
        assert actual_packet.HasField('session_id')
        assert actual_packet.HasField('payload')

        actual_payload = Foo()
        actual_payload.ParseFromString(actual_packet.payload.value)

        assert actual_payload.data == expected_data

    def test_send_close(self, SimpleModel, make_endpoint, timeout):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        sent_data = []

        def send(data, identities):
            """Send-callback stub that appends send packet to the list."""
            nonlocal sent_data
            packet = Packet()
            packet.ParseFromString(data)
            sent_data.append((packet, identities))
            return identities

        expected_service_id = 1
        expected_method_id = 1

        endpoint: Endpoint = make_endpoint(
            service_id=expected_service_id,
            method_id=expected_method_id,
            message_cls=Foo,
            send=send,
            model=SimpleModel()
        )

        expected_to_identity = to_identity = 'to_identity'
        endpoint.send(is_close=True, identity=to_identity)

        assert wait_until(
            lambda: len([1 for p, _ in sent_data if not p.is_heartbeat]) > 0,
            timeout=timeout
        )

        assert len(sent_data) == 1
        actual_packet, actual_to_identities = sent_data[0]

        assert actual_to_identities == [expected_to_identity]

        assert actual_packet.is_initial
        assert actual_packet.is_closing
        assert not actual_packet.is_error
        assert actual_packet.HasField('session_id')
        assert not actual_packet.HasField('payload')

    def test_receive_message(self, SimpleModel, make_endpoint, timeout):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        received_data = []

        def receive(identity, message):
            """Receive-callback stub that appends send packet to the list."""
            nonlocal received_data
            received_data.append((identity, message))

        endpoint: Endpoint = make_endpoint(
            service_id=1,
            method_id=1,
            message_cls=Foo,
            send=lambda _, identities: identities,
            model=SimpleModel()
        )
        endpoint.on_receive(receive)

        request = Foo()
        expected_data = request.data = 'test_data'
        expected_from_identity = from_identity = 'test_from_identity'

        packet = Packet()
        packet.service_id = 1
        packet.method_id = 1
        packet.is_initial = True
        packet.packet_id = 1
        packet.window_start = 1
        packet.payload.value = request.SerializeToString()
        packet.session_id.value = b'test_session_id'

        endpoint.consume_packet(
            from_identity=from_identity,
            packet=packet
        )

        assert wait_until(lambda: len(received_data) > 0, timeout=timeout)

        assert len(received_data) == 1
        actual_identity, actual_message = received_data[0]

        assert actual_identity == expected_from_identity
        assert actual_message.data == expected_data

    def test_receive_close(self, SimpleModel, make_endpoint, timeout):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        endpoint: Endpoint = make_endpoint(
            service_id=1,
            method_id=1,
            message_cls=Foo,
            send=lambda _, identities: identities,
            model=SimpleModel()
        )
        packet = Packet()
        packet.service_id = 1
        packet.method_id = 1
        packet.is_initial = True
        packet.is_closing = True
        packet.packet_id = 1
        packet.window_start = 1
        packet.session_id.value = b'test_session_id'

        from_identity = 'test_from_identity'
        endpoint.consume_packet(
            from_identity=from_identity,
            packet=packet
        )

        wait_until(lambda: endpoint.is_closed, timeout=timeout)

        assert endpoint.is_closed

    def test_heartbeats(
        self,
        SimpleModel,
        make_endpoint,
        timeout,
        time
    ):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        heartbeat_interval = 0.05
        sent_data = []

        def send(data, identities):
            """Send-callback stub that appends send packet to the list."""
            nonlocal sent_data
            packet = Packet()
            packet.ParseFromString(data)
            sent_data.append((packet, identities))
            return identities

        endpoint: Endpoint = make_endpoint(
            service_id=1,
            method_id=1,
            message_cls=Foo,
            send=send,
            model=SimpleModel(),
            heartbeat_interval=heartbeat_interval
        )
        packet = Packet()
        packet.service_id = 1
        packet.method_id = 1
        packet.is_initial = True
        packet.packet_id = 1
        packet.window_start = 1
        packet.session_id.value = b'test_session_id'

        from_identity = 'test_from_identity'
        endpoint.consume_packet(
            from_identity=from_identity,
            packet=packet
        )

        assert wait_until(
            lambda: len(endpoint.remote_peers) > 0,
            timeout=timeout
        )

        time.return_value = time() + heartbeat_interval + 100

        assert wait_until(
            lambda: any(p.is_heartbeat for p, _, in sent_data),
            timeout=timeout
        )

    def test_alive(
        self,
        SimpleModel,
        make_endpoint,
        timeout,
        time
    ):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        alive_timeout = 0.05

        actual_identity = None

        def peer_lost(identity):
            """Peer-callback."""
            nonlocal actual_identity
            actual_identity = identity

        endpoint: Endpoint = make_endpoint(
            service_id=1,
            method_id=1,
            message_cls=Foo,
            send=lambda _, identities: identities,
            model=SimpleModel(),
            alive_timeout=alive_timeout
        )
        endpoint.on_peer_lost(peer_lost)
        packet = Packet()
        packet.service_id = 1
        packet.method_id = 1
        packet.is_initial = True
        packet.packet_id = 1
        packet.window_start = 1
        packet.session_id.value = b'test_session_id'

        from_identity = 'test_from_identity'
        endpoint.consume_packet(
            from_identity=from_identity,
            packet=packet
        )

        time.return_value = time() + alive_timeout + 100

        assert wait_until(
            lambda: actual_identity is None,
            timeout=timeout
        )

    def test_send_message_with_acknowledgement(
        self,
        AcknowledgementModel,
        make_endpoint,
        timeout
    ):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        sent_data = []

        def send(data, identities):
            """Send-callback stub that appends send packet to the list."""
            nonlocal sent_data
            packet = Packet()
            packet.ParseFromString(data)
            sent_data.append((packet, identities))
            return identities

        expected_service_id = 1
        expected_method_id = 1

        endpoint: Endpoint = make_endpoint(
            service_id=expected_service_id,
            method_id=expected_method_id,
            message_cls=Foo,
            send=send,
            model=AcknowledgementModel()
        )

        request = Foo()
        expected_data = request.data = 'test_data'
        expected_to_identity = to_identity = 'to_identity'
        endpoint.send(message=request, identity=to_identity)

        assert wait_until(
            lambda: len([1 for p, _ in sent_data if not p.is_heartbeat]) > 0,
            timeout=timeout
        )

        assert len(sent_data) == 1
        actual_packet, actual_to_identities = sent_data[0]

        assert actual_to_identities == [expected_to_identity]

        assert actual_packet.is_initial
        assert actual_packet.acknowledgement_required
        assert not actual_packet.is_closing
        assert not actual_packet.is_error
        assert actual_packet.HasField('session_id')
        assert actual_packet.HasField('payload')

        actual_payload = Foo()
        actual_payload.ParseFromString(actual_packet.payload.value)

        assert actual_payload.data == expected_data

    def test_resend(
        self,
        AcknowledgementModel,
        make_endpoint,
        timeout,
        acknowledgement_interval,
        time
    ):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        sent_data = []

        def send(data, identities):
            """Send-callback stub that appends send packet to the list."""
            nonlocal sent_data
            packet = Packet()
            packet.ParseFromString(data)
            sent_data.append((packet, identities))
            return identities

        expected_service_id = 1
        expected_method_id = 1

        endpoint: Endpoint = make_endpoint(
            service_id=expected_service_id,
            method_id=expected_method_id,
            message_cls=Foo,
            send=send,
            model=AcknowledgementModel()
        )

        request = Foo()
        expected_to_identity = to_identity = 'to_identity'
        endpoint.send(message=request, identity=to_identity)

        assert wait_until(
            lambda: len([1 for p, _ in sent_data if not p.is_heartbeat]) > 0,
            timeout=timeout
        )
        packet_id = next(
            p.packet_id for p, _ in sent_data if not p.is_heartbeat
        )
        time.return_value = time() + acknowledgement_interval + 10

        assert wait_until(
            lambda: len([
                1 for p, _ in sent_data if p.packet_id == packet_id
            ]) >= 2,
            timeout=timeout
        )
        initial_resent_packet, initial_identities = [
            (p, is_) for p, is_ in sent_data
            if p.packet_id == packet_id
        ][0]
        actual_resent_packet, actual_identities = [
            (p, is_) for p, is_ in sent_data
            if p.packet_id == packet_id
        ][1]
        assert (initial_resent_packet.session_id.value ==
                actual_resent_packet.session_id.value)
        assert (initial_resent_packet.packet_id ==
                actual_resent_packet.packet_id)
        assert (initial_resent_packet.payload.value ==
                actual_resent_packet.payload.value)
        assert initial_identities == actual_identities
        assert actual_identities == [expected_to_identity]

    def test_receive_message_with_acknowledgement(
        self,
        AcknowledgementModel,
        make_endpoint,
        timeout
    ):
        """Test simple message sending.

        Endpoint correctly forms a packet with the payload and passes it
        to the specified identity.
        """
        received_data = []
        sent_data = []
        session_id = b'test_session_id'

        def receive(identity, message):
            """Receive-callback stub."""
            nonlocal received_data
            received_data.append((identity, message))

        def send(data, identities):
            """Send-callback stub that appends send packet to the list."""
            packet = Packet()
            packet.ParseFromString(data)
            sent_data.append((packet, identities))
            return identities

        endpoint: Endpoint = make_endpoint(
            service_id=1,
            method_id=1,
            session_id=session_id,
            message_cls=Foo,
            send=send,
            model=AcknowledgementModel()
        )
        endpoint.on_receive(receive)

        request = Foo()
        expected_data = request.data = 'test_data'
        expected_from_identity = from_identity = 'test_from_identity'

        packet = Packet()
        packet.service_id = 1
        packet.method_id = 1
        packet.packet_id = 1
        packet.window_start = 1
        packet.is_initial = True
        packet.acknowledgement_required = True
        packet.payload.value = request.SerializeToString()
        packet.session_id.value = session_id

        endpoint.consume_packet(
            from_identity=from_identity,
            packet=packet
        )

        wait_until(lambda: len(received_data) > 0, timeout=timeout)

        assert len(received_data) == 1
        actual_identity, actual_message = received_data[0]
        assert actual_identity == expected_from_identity
        assert actual_message.data == expected_data

        assert wait_until(
            lambda: len([1 for p, _ in sent_data if p.acknowledges]) > 0,
            timeout=timeout
        )
        actual_packet, actual_identities = next(
            (p, is_) for p, is_ in sent_data if p.acknowledges
        )
        assert actual_packet.acknowledges == [packet.packet_id]
        assert actual_packet.session_id.value == packet.session_id.value
        assert actual_packet.packet_id != packet.packet_id
        assert actual_identities == [from_identity]

    @pytest.fixture(name='SimpleModel')
    def simple_model(self):
        """Simple model."""
        # pylint: disable=missing-docstring
        class SimpleModel(Model):
            ID = 'SIMPLE'
            SINGLETON_SESSION = False

            class LocalState(enum.Enum):
                ACTIVE = 'ACTIVE'
                CLOSED = 'CLOSED'

            LOCAL_BEGIN = LocalState['ACTIVE']
            LOCAL_END = LocalState['CLOSED']
            LOCAL_TRANSITIONS = [
                Model.Transition(
                    name='Close',
                    condition='CLOSE or INBOUND_CLOSE',
                    sources={LocalState['ACTIVE']},
                    destination=LOCAL_END,
                    actions=set()
                ),
            ]

            class RemoteState(enum.Enum):
                ACTIVE = 'ACTIVE'
                CLOSED = 'CLOSED'

            REMOTE_BEGIN = RemoteState['ACTIVE']
            REMOTE_END = RemoteState['CLOSED']
            REMOTE_TRANSITIONS = [
                Model.Transition(
                    name='Send payload',
                    condition=(
                        'OUTBOUND_PAYLOAD and '
                        'not OUTBOUND_CLOSE and '
                        'TO_ONE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={Action.SEND_PAYLOAD, Action.SEND_TO_ONE}
                ),
                Model.Transition(
                    name='Send close',
                    condition=(
                        'OUTBOUND_CLOSE and '
                        'not OUTBOUND_PAYLOAD and '
                        'TO_ONE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={Action.SEND_CLOSE, Action.SEND_TO_ONE}
                ),
                Model.Transition(
                    name='Send payload and close',
                    condition=(
                        'OUTBOUND_CLOSE and '
                        'OUTBOUND_PAYLOAD and '
                        'TO_ONE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={
                        Action.SEND_PAYLOAD,
                        Action.SEND_CLOSE,
                        Action.SEND_TO_ONE
                    }
                ),
                Model.Transition(
                    name='Receive payload',
                    condition=(
                        'INBOUND_PAYLOAD and '
                        'not INBOUND_CLOSE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={Action.PROCESS_INBOUND_PAYLOAD}
                ),
                Model.Transition(
                    name='Receive inbound close',
                    condition=(
                        'INBOUND_CLOSE and '
                        'not INBOUND_PAYLOAD'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=REMOTE_END,
                    actions=set()
                ),
                Model.Transition(
                    name='Receive inbound payload and close',
                    condition=(
                        'INBOUND_PAYLOAD and '
                        'INBOUND_CLOSE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=REMOTE_END,
                    actions={Action.PROCESS_INBOUND_PAYLOAD}
                ),
                Model.Transition(
                    name='Close',
                    condition='LOCAL_CLOSED and not INBOUND_CLOSE',
                    sources={Model.ANY},
                    destination=REMOTE_END,
                    actions=set()
                )
            ]

        return SimpleModel

    @pytest.fixture(name='AcknowledgementModel')
    def acknowledgement_model(self):
        """Model that uses acknowledgement."""
        # pylint: disable=missing-docstring
        class AcknowledgementModel(Model):
            ID = 'ACKNOWLEDGE'
            SINGLETON_SESSION = False

            class LocalState(enum.Enum):
                ACTIVE = 'ACTIVE'
                CLOSED = 'CLOSED'

            LOCAL_BEGIN = LocalState['ACTIVE']
            LOCAL_END = LocalState['CLOSED']
            LOCAL_TRANSITIONS = [
                Model.Transition(
                    name='Accept peer',
                    condition='NEW_OUTBOUND_PEER or NEW_INBOUND_PEER',
                    sources={LocalState['ACTIVE']},
                    destination=Model.ANY,
                    actions=set()
                ),
                Model.Transition(
                    name='Close',
                    condition='CLOSE or INBOUND_CLOSE',
                    sources={LocalState['ACTIVE']},
                    destination=LOCAL_END,
                    actions=set()
                ),
            ]

            class RemoteState(enum.Enum):
                ACTIVE = 'ACTIVE'
                CLOSED = 'CLOSED'

            REMOTE_BEGIN = RemoteState['ACTIVE']
            REMOTE_END = RemoteState['CLOSED']
            REMOTE_TRANSITIONS = [
                Model.Transition(
                    name='Send payload',
                    condition=(
                        'OUTBOUND_PAYLOAD and '
                        'not OUTBOUND_CLOSE and '
                        'TO_ONE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={
                        Action.SEND_PAYLOAD,
                        Action.SEND_TO_ONE,
                        Action.REQUIRE_ACKNOWLEDGEMENT
                    }
                ),
                Model.Transition(
                    name='Send close',
                    condition=(
                        'OUTBOUND_CLOSE and '
                        'not OUTBOUND_PAYLOAD and '
                        'TO_ONE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={
                        Action.SEND_CLOSE,
                        Action.SEND_TO_ONE,
                        Action.REQUIRE_ACKNOWLEDGEMENT
                    }
                ),
                Model.Transition(
                    name='Send payload and close',
                    condition=(
                        'OUTBOUND_CLOSE and '
                        'OUTBOUND_PAYLOAD and '
                        'TO_ONE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={
                        Action.SEND_PAYLOAD,
                        Action.SEND_CLOSE,
                        Action.SEND_TO_ONE,
                        Action.REQUIRE_ACKNOWLEDGEMENT
                    }
                ),
                Model.Transition(
                    name='Receive payload',
                    condition=(
                        'INBOUND_PAYLOAD and '
                        'not INBOUND_CLOSE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=Model.ANY,
                    actions={Action.PROCESS_INBOUND_PAYLOAD}
                ),
                Model.Transition(
                    name='Receive inbound close',
                    condition=(
                        'INBOUND_CLOSE and '
                        'not INBOUND_PAYLOAD'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=REMOTE_END,
                    actions=set()
                ),
                Model.Transition(
                    name='Receive inbound payload and close',
                    condition=(
                        'INBOUND_PAYLOAD and '
                        'INBOUND_CLOSE'
                    ),
                    sources={RemoteState['ACTIVE']},
                    destination=REMOTE_END,
                    actions={Action.PROCESS_INBOUND_PAYLOAD}
                ),
                Model.Transition(
                    name='Close',
                    condition='LOCAL_CLOSED and not INBOUND_CLOSE',
                    sources={Model.ANY},
                    destination=REMOTE_END,
                    actions=set()
                )
            ]

        return AcknowledgementModel

    @pytest.fixture
    def receiver_window_size(self):
        return 100

    @pytest.fixture
    def sender_window_size(self):
        return 100

    @pytest.fixture
    def acknowledgement_interval(self):
        return 30.0

    @pytest.fixture
    def heartbeat_interval(self):
        return 5.0

    @pytest.fixture
    def alive_timeout(self):
        return 30.0

    @pytest.fixture
    def time(self):
        return Mock(wraps=timelib.time)

    @pytest.fixture
    def make_endpoint(
        self,
        sender_window_size,
        receiver_window_size,
        acknowledgement_interval,
        heartbeat_interval,
        alive_timeout,
        time
    ):
        """Convenience endpoint factory."""
        def make_endpoint_(
            service_id,
            method_id,
            send,
            message_cls,
            model,
            session_id=None,
            acknowledgement_interval=acknowledgement_interval,
            heartbeat_interval=heartbeat_interval,
            alive_timeout=alive_timeout,
            sender_window_size=sender_window_size,
            receiver_window_size=receiver_window_size,
            time=time
        ):
            return Endpoint(
                service_id=service_id,
                method_id=method_id,
                model=model,
                message_cls=message_cls,
                session_id=session_id,
                acknowledgement_interval=acknowledgement_interval,
                heartbeat_interval=heartbeat_interval,
                alive_timeout=alive_timeout,
                send=send,
                time=time,
                receiver_window_size=receiver_window_size,
                sender_window_size=sender_window_size
            )

        make_endpoint_.__name__ = 'make_endpoint'
        return make_endpoint_
