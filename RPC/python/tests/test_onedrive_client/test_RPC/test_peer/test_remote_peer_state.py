"""Tests for ``RemotePeerState`` class."""
import enum
import time as timelib
from unittest.mock import Mock

import pytest

from onedrive_client.RPC.models import Action, Model
from onedrive_client.RPC.peer.remote_peer_state import RemotePeerState
from onedrive_client.RPC.peer.window import ReceiverWindow
from onedrive_client.RPC.RPC_pb2 import Packet
# pylint: disable=too-many-public-methods


class TestRemotePeerState:
    """Tests for ``RemotePeerState`` class."""
    # pylint: disable=no-self-use,invalid-name,no-member
    def test_last_heartbeat_sent(
        self,
        remote_peer_state: RemotePeerState,
        time
    ):
        """``last_heartbeat_sent`` attribute is updated on outbound packet.

        When any packet is sent - ``last_heartbeat_sent`` should be updated
        to signify last time of communication with the remote peer.
        """
        packet = Packet()
        actual_last_heartbeat_sent_time = remote_peer_state.last_heartbeat_sent
        expected_last_heartbeat_sent_time = time.return_value = (
            actual_last_heartbeat_sent_time + 100
        )

        remote_peer_state.process_outbound_packet(
            packet=packet
        )
        assert remote_peer_state.last_heartbeat_sent == (
            expected_last_heartbeat_sent_time
        )

    def test_is_heartbeat_interval_exceeded(
        self,
        remote_peer_state: RemotePeerState,
        heartbeat_interval,
        time
    ):
        """Basic test of ``is_heartbeat_interval_exceeded`` property.

        ``is_heartbeat_interval_exceeded`` returns ``True`` value when
        heartbeat-interval passed since last packet was sent to the peer.
        """
        packet = Packet()
        remote_peer_state.process_outbound_packet(packet=packet)

        last_heartbeat_sent_time = remote_peer_state.last_heartbeat_sent
        time.return_value = (
            last_heartbeat_sent_time +
            heartbeat_interval +
            1
        )
        assert remote_peer_state.is_heartbeat_interval_exceeded

    def test_is_heartbeat_interval_exceeded_negative(
        self,
        remote_peer_state: RemotePeerState,
        heartbeat_interval,
        time
    ):
        """Basic negative test test of ``is_heartbeat_interval_exceeded``.

        ``is_heartbeat_interval_exceeded`` returns ``False`` value when
        heartbeat-interval is not yet passed since last packet was sent to the
        peer.
        """
        packet = Packet()
        remote_peer_state.process_outbound_packet(packet=packet)

        last_heartbeat_sent_time = remote_peer_state.last_heartbeat_sent
        time.return_value = (
            last_heartbeat_sent_time +
            heartbeat_interval -
            1
        )
        assert not remote_peer_state.is_heartbeat_interval_exceeded

    def test_is_alive_timeout_exceeded(
        self,
        remote_peer_state: RemotePeerState,
        alive_timeout,
        time
    ):
        """Basic test of ``is_alive_timeout_exceeded`` property.

        ``is_alive_timeout_exceeded`` returns ``True`` if alive-timeout time
        has been passed since last packet was received from the peer.
        """
        packet = Packet()
        packet.packet_id = remote_peer_state.receiver_window.start
        packet.window_start = remote_peer_state.receiver_window.start
        remote_peer_state.process_inbound_packet(packet=packet)

        last_activity = remote_peer_state.last_activity
        time.return_value = (
            last_activity +
            alive_timeout +
            1
        )
        assert remote_peer_state.is_alive_timeout_exceeded

    def test_is_alive_timeout_exceeded_negative(
        self,
        remote_peer_state: RemotePeerState,
        alive_timeout,
        time
    ):
        """Basic negative test of ``is_alive_timeout_exceeded`` property.

        ``is_alive_timeout_exceeded`` returns ``False`` if alive-timeout time
        has not been passed yet since last packet was received from the peer.
        """
        packet = Packet()
        packet.packet_id = remote_peer_state.receiver_window.start
        packet.window_start = remote_peer_state.receiver_window.start
        remote_peer_state.process_inbound_packet(packet=packet)

        last_activity = remote_peer_state.last_activity
        time.return_value = (
            last_activity +
            alive_timeout -
            1
        )
        assert not remote_peer_state.is_alive_timeout_exceeded

    def test_packets_to_resend(
        self,
        remote_peer_state: RemotePeerState,
        time,
        acknowledgement_interval
    ):
        """``packets_to_resend`` yields packets to for re-sending.

        When a packet that requires acknowledgement was sent and
        acknowledgement interval was passed and the packet wasn't acknowledged
        - the packet must be yielded by ``packets_to_resend`` method as a
        packet that needs to be resent.
        """
        packet = Packet()
        packet.packet_id = 123456
        packet.acknowledgement_required = True

        remote_peer_state.process_outbound_packet(packet=packet)
        time.return_value = time() + acknowledgement_interval + 100

        expected_packet_ids = {packet.packet_id}
        actual_packets_ids = set(
            p.packet_id for p in remote_peer_state.packets_to_resend
        )
        assert actual_packets_ids == expected_packet_ids

    def test_packets_to_resend_updates_time(
        self,
        remote_peer_state: RemotePeerState,
        time,
        acknowledgement_interval
    ):
        """``process_outbound_packet()`` updates time when packet last sent.

        ``process_outbound_packet()`` should update timestamp when the packet
        that requires acknowledgement is sent last time and
        ``packets_to_resend`` should not yield packets for which the
        acknowledgement interval is not exceeded.
        """
        packet = Packet()
        packet.packet_id = 123456
        packet.acknowledgement_required = True

        remote_peer_state.process_outbound_packet(packet=packet)
        time.return_value = time() + acknowledgement_interval + 100

        remote_peer_state.process_outbound_packet(packet=packet)
        time.return_value = time() + acknowledgement_interval - 1

        actual_packets_ids = set(
            p.packet_id for p in remote_peer_state.packets_to_resend
        )
        assert len(actual_packets_ids) == 0

    def test_process_inbound_packet_updates(
        self,
        remote_peer_state: RemotePeerState,
        time
    ):
        """``process_inbound_packet()`` updates ``last_activity`` attribute."""
        packet = Packet()
        packet.packet_id = remote_peer_state.receiver_window.start

        last_activity_before = remote_peer_state.last_activity

        expected_last_activity = time.return_value = (
            last_activity_before + 1000
        )
        remote_peer_state.process_inbound_packet(packet=packet)

        assert remote_peer_state.last_activity == expected_last_activity

    def test_process_inbound_packet_skips_packet_if_stale(
        self,
        remote_peer_state: RemotePeerState,
        SimpleModel
    ):
        """``process_inbound_packet()`` skips packet if the peer is "stale"."""
        packet = Packet()
        packet.packet_id = remote_peer_state.receiver_window.start

        remote_peer_state.current_state = SimpleModel.REMOTE_END
        assert remote_peer_state.is_stale

        actual_result = remote_peer_state.process_inbound_packet(packet=packet)

        assert not actual_result

    def test_process_inbound_packet_skips_packet_if_already_received(
        self,
        remote_peer_state: RemotePeerState
    ):
        """``process_inbound_packet()`` skips already received packets."""
        packet = Packet()
        packet.packet_id = remote_peer_state.receiver_window.start
        packet.window_start = remote_peer_state.receiver_window.start

        actual_result = remote_peer_state.process_inbound_packet(packet=packet)
        assert actual_result

        actual_result = remote_peer_state.process_inbound_packet(packet=packet)
        assert not actual_result

    def test_unacknowledged_received_packets_returns_unacknowledged_packets(
        self,
        remote_peer_state: RemotePeerState
    ):
        """``unacknowledged_received_packets()`` returns packets that require
        acknowledgement.
        """
        packet = Packet()
        packet.packet_id = remote_peer_state.receiver_window.start
        packet.window_start = remote_peer_state.receiver_window.start
        packet.acknowledgement_required = True

        actual_result = remote_peer_state.process_inbound_packet(packet=packet)
        assert actual_result

        expected_packet_ids = {packet.packet_id}
        actual_packet_ids = remote_peer_state.unacknowledged_received_packets

        assert actual_packet_ids == expected_packet_ids

    def test_process_outbound_packet_clears_unacknowledged_received_packets(
        self,
        remote_peer_state: RemotePeerState
    ):
        """``process_outbound_packet()`` clears unack-ed received packets.

        When a packet that requires acknowledgement is received and than
        a packet that acknowledges it is sent
        ``unacknowledged_received_packets`` should not return the ID
        of the initially received packet.
        """
        inbound_packet = Packet()
        inbound_packet.packet_id = remote_peer_state.receiver_window.start
        inbound_packet.window_start = remote_peer_state.receiver_window.start
        inbound_packet.acknowledgement_required = True

        actual_result = remote_peer_state.process_inbound_packet(
            packet=inbound_packet
        )
        assert actual_result

        outbound_packet = Packet()
        outbound_packet.acknowledges.append(inbound_packet.packet_id)

        remote_peer_state.process_outbound_packet(packet=outbound_packet)

        actual_packet_ids = remote_peer_state.unacknowledged_received_packets

        assert len(actual_packet_ids) == 0

    def test_process_inbound_packet_skips_packet_if_packet_id_not_in_window(
        self,
        remote_peer_state: RemotePeerState
    ):
        """``process_inbound_packet()`` moves window start if needed."""
        window = ReceiverWindow(
            start=remote_peer_state.receiver_window.start,
            size=len(remote_peer_state.receiver_window)
        )
        window.move(list(window)[1])
        packet_id = list(window)[-1]

        packet = Packet()
        packet.packet_id = packet_id
        packet.window_start = remote_peer_state.receiver_window.start

        actual_result = remote_peer_state.process_inbound_packet(
            packet=packet
        )
        assert not actual_result

    def test_process_inbound_packet_handles_inbound_acknowledgements(
        self,
        remote_peer_state: RemotePeerState
    ):
        """``process_inbound_packet()`` handles inbound acknowledgements."""
        outbound_packet = Packet()
        outbound_packet.acknowledgement_required = True

        remote_peer_state.process_outbound_packet(
            packet=outbound_packet
        )

        inbound_packet = Packet()
        inbound_packet.packet_id = remote_peer_state.receiver_window.start
        inbound_packet.window_start = remote_peer_state.receiver_window.start
        inbound_packet.acknowledges.append(outbound_packet.packet_id)

        actual_result = remote_peer_state.process_inbound_packet(
            packet=inbound_packet
        )
        assert actual_result

        assert not remote_peer_state.unacknowledged_sent_packets

    @pytest.fixture(name='SimpleModel')
    def simple_model(self):
        """Simple generic model."""
        # pylint: disable=missing-docstring
        class SimpleModel(Model):
            ID = 'SIMPLE'
            SINGLETON_SESSION = False

            class LocalState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            LOCAL_BEGIN = LocalState['IDLE']
            LOCAL_END = LocalState['CLOSED']
            LOCAL_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='NEW_INBOUND_PEER',
                    sources={LocalState['IDLE']},
                    destination=LocalState['FOO'],
                    actions=set()
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={LocalState['FOO']},
                    destination=LocalState['CLOSED'],
                    actions={Action.SEND_CLOSE, Action.SEND_TO_ALL}
                )
            ]

            class RemoteState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            REMOTE_BEGIN = RemoteState['IDLE']
            REMOTE_END = RemoteState['CLOSED']
            REMOTE_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='INBOUND_INITIAL',
                    sources={RemoteState['IDLE']},
                    destination=RemoteState['FOO'],
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={RemoteState['FOO']},
                    destination=RemoteState['CLOSED'],
                    actions=set()
                )
            ]

        return SimpleModel

    @pytest.fixture
    def receiver_window_size(self):
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
    def remote_peer_state(
        self,
        SimpleModel,
        receiver_window_size,
        acknowledgement_interval,
        heartbeat_interval,
        alive_timeout,
        time
    ):
        """Simple generic ``RemotePeerState`` instance."""
        model = SimpleModel()
        remote_peer_state_ = RemotePeerState(
            identity='test_identity',
            model=model,
            receiver_window_size=receiver_window_size,
            receiver_window_start=1,
            acknowledgement_interval=acknowledgement_interval,
            heartbeat_interval=heartbeat_interval,
            alive_timeout=alive_timeout,
            time=time
        )
        assert not remote_peer_state_.is_stale
        assert not remote_peer_state_.is_closed

        return remote_peer_state_
