"""Provides ``RemotePeerState`` class."""
import time as timelib
from typing import Callable, Dict, List, Optional, Set

import gevent
import gevent.event
import gevent.lock
import gevent.queue

from .window import ReceiverWindow, UnknownID
from ..models import Model
from ..RPC_pb2 import Packet
from ..utils.logbook import Logger

LOGGER = Logger(__name__)


class RemotePeerState:
    """Utility class that represents the state of a single remote peer.

    This class was created to factor out all the state related to remote peers
    from ``Endpoint`` class.
    """
    def __init__(
        self,
        identity: str,
        model: Model,
        receiver_window_size: int,
        receiver_window_start: int = None,
        acknowledgement_interval: Optional[float] = None,
        heartbeat_interval: Optional[float] = None,
        alive_timeout: Optional[float] = None,
        time: Callable[[], float] = timelib.time
    ):
        self.identity                   = identity
        self.is_accepted                = False
        self.__model                    = model
        self.current_state              = self.__model.REMOTE_BEGIN
        self.__acknowledgement_interval = acknowledgement_interval
        self.__heartbeat_interval       = heartbeat_interval
        self.__alive_timeout            = alive_timeout
        self.__time                     = time
        self.receiver_window            = ReceiverWindow(
            size=receiver_window_size,
            start=receiver_window_start
        )
        self.send_queue                 = gevent.queue.JoinableQueue()

        self.last_activity       : float             = 0.0
        self.last_heartbeat_sent : float             = 0.0
        self.is_registered       : bool              = False
        self.initial_packet_id   : int               = None
        self.__is_registered     : bool              = False
        self.__lock              : gevent.lock.RLock = gevent.lock.RLock()

        self.__sent_unacknowledged_packets: Dict[int, List[Packet, float]] = {}
        self.__received_unacknowledged_packets: Set = set()

        self.__logger = Logger(
            __name__,
            processor=lambda record: record.extra.update(
                identity=self.identity,
                current_window_start=self.receiver_window.start
            )
        )

    def accept(self):
        """"Accept" the peer.

        It happens when new peer is created and REJECT action is not
        returned by the state machine.
        """
        self.is_accepted = True

    @property
    def is_closed(self):
        """Whether peer is in halted state."""
        return self.__model.is_halted_remote(self.current_state)

    @property
    def is_stale(self):
        """Whether the peer is closed and have no outstanding packets."""
        return (
            self.current_state == self.__model.REMOTE_END and
            len(self.__received_unacknowledged_packets) == 0 and
            len(self.__sent_unacknowledged_packets) == 0 and
            len(self.send_queue) == 0
        )

    @property
    def packets_to_resend(self):
        """Unacknowledged sent packets that are ready for re-sending."""
        results = []
        current_time = self.__time()
        items = dict(self.__sent_unacknowledged_packets).items()
        for _, (packet, time) in items:
            if (current_time - time) > self.__acknowledgement_interval:
                results.append(packet)
        return results

    @property
    def unacknowledged_sent_packets(self):
        """Sent packets that are still not acknowledged."""
        return list(self.__sent_unacknowledged_packets.keys())

    @property
    def unacknowledged_received_packets(self):
        """Received packets that still require acknowledgement."""
        return set(self.__received_unacknowledged_packets)

    @property
    def is_heartbeat_interval_exceeded(self):
        """Whether heartbeat interval interval is exceeded.

        It is counted from the time when last packet was sent to this peer.
        """
        return ((self.__time() - self.last_heartbeat_sent) >
                self.__heartbeat_interval)

    @property
    def is_alive_timeout_exceeded(self):
        """Whether alive-timeout exceeded.

        It is counted from the time when the last packet was received from
        the peer.
        """
        return ((self.__time() - self.last_activity) >
                self.__alive_timeout)

    def process_inbound_packet(self, packet: Packet) -> bool:
        """Process a packet received from the remote peer."""
        extra = {
            'packet_id': packet.packet_id,
            'window_start': packet.window_start
        }
        self.__logger.trace('Processing inbound packet...', extra=extra)
        with self.__lock:
            # If the peer is "stale" - it's dead, skip processing entirely.
            if self.is_stale:
                self.__logger.trace(
                    'The peer is stale.',
                    extra=extra
                )
                return False

            # Update last activity.
            # It comes first because any activity is counted as a sign that
            # the peer is "active" or "alive".
            self.last_activity = self.__time()

            # The packet was already received - skip it.
            if self.receiver_window.is_received(packet.packet_id):
                self.__logger.trace(
                    'Packet was already received.',
                    extra=extra
                )
                return False

            # If the inbound packet requires acknowledgement -
            # schedule the acknowledgement to be sent.
            if packet.acknowledgement_required:
                self.__received_unacknowledged_packets.add(packet.packet_id)

            try:
                # Move the window according to the window-start specified in
                # the packet.
                self.receiver_window.move(packet.window_start)
            except UnknownID:
                # The packet's window-start precedes the current window-start
                # or is too further forward to the current window-start.
                self.__logger.trace(
                    'Packet ID is not known to receiver-window.',
                    extra=extra
                )
                return False

            # If the packet is not in the window - it might been already
            # received. Or the receiver-window is too small.
            if packet.packet_id not in self.receiver_window:
                return False

            # Mark the packet as received.
            self.receiver_window.receive(packet.packet_id)

            # "Forget" the sent packets that are acknowledged by the
            # inbound packet.
            for packet_id in packet.acknowledges:
                self.__sent_unacknowledged_packets.pop(packet_id, None)

            self.__logger.trace(
                'Packet is successfully processed.',
                extra=extra
            )
            return True

    def process_outbound_packet(self, packet: Packet):
        """Handles packets sent the remote peer."""
        extra = {
            'packet_id': packet.packet_id,
            'window_start': packet.window_start
        }
        self.__logger.debug('Processing outbound packet...', extra=extra)
        with self.__lock:
            # Set or update time of last time when a packet
            # that requires acknowledgement is sent.
            if packet.acknowledgement_required:
                if packet.packet_id in self.__sent_unacknowledged_packets:
                    self.__logger.trace(
                        'Updating time for already sent packet with '
                        'acknowledgement.', extra=extra
                    )
                    self.__sent_unacknowledged_packets[packet.packet_id][1] = \
                        self.__time()
                else:
                    self.__logger.trace(
                        'New packet with acknowledgement.', extra=extra
                    )
                    self.__sent_unacknowledged_packets[packet.packet_id] = [
                        packet, self.__time()
                    ]

            # Update last time packet was sent to the peer.
            self.last_heartbeat_sent = self.__time()

            # If the packet contains acknowledgements - "forget" these packets.
            for packet_id in packet.acknowledges:
                self.__received_unacknowledged_packets.discard(packet_id)
