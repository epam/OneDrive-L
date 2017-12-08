"""Tests for sender- and receiver- windows."""
import random as rnd

import pytest

from onedrive_client.RPC.peer.window import (
    next_packet_id,
    ReceiverWindow,
    SenderWindow,
    UnknownID
)


class TestSenderWindow:
    """Tests of ``SenderWindow`` class."""
    # pylint: disable=no-self-use
    def test_send(self):
        """Basic test of ``send()`` method.

        ``send()`` exclude the ID from the list of free IDs and
        makes it "sent".
        """
        window = SenderWindow(100)

        packet_id = rnd.choice(list(window))
        window.send(packet_id=packet_id)

        assert packet_id not in set(window.free_ids())
        assert not window.is_cleared(packet_id=packet_id)
        assert window.is_sent(packet_id=packet_id)

    def test_clear(self):
        """Basic test of ``clear()`` method.

        ``clear()``
        """
        window = SenderWindow(100)

        packet_id = rnd.choice(list(window))
        window.send(packet_id=packet_id)

        assert window.is_sent(packet_id=packet_id)
        assert not window.is_cleared(packet_id=packet_id)

        window.clear(packet_id=packet_id)

        assert window.is_cleared(packet_id=packet_id)
        assert packet_id in set(window)
        assert packet_id not in set(window.free_ids())

    def test_clear_starting_packet(self):
        """When a starting packet is cleared - the window should be moved."""
        window_size = 100
        window = SenderWindow(window_size)

        expected_new_starting_packet_id = list(window)[1]
        starting_packet_id = window.start
        window.send(packet_id=starting_packet_id)

        assert window.is_sent(packet_id=starting_packet_id)
        assert not window.is_cleared(packet_id=starting_packet_id)

        window.clear(packet_id=starting_packet_id)

        assert not window.is_cleared(packet_id=starting_packet_id)
        assert starting_packet_id not in set(window)
        assert starting_packet_id not in set(window.free_ids())

        assert len(list(window.free_ids())) == window_size
        assert list(window.free_ids()) == list(window)
        assert window.start == list(window)[0]
        assert window.start == expected_new_starting_packet_id

    def test_move(self):
        """Simple window-move test."""
        window_size = 100
        window = SenderWindow(window_size)

        expected_starting_packet_id = list(window)[50]
        previous_start = window.start

        window.move(packet_id=expected_starting_packet_id)

        assert window.start == expected_starting_packet_id
        assert list(window)[0] == expected_starting_packet_id
        assert len(list(window)) == window_size
        assert window.start != previous_start


class TestReceiverWindow:
    """Tests for ``ReceiverWindow`` class."""
    # pylint: disable=no-self-use
    def test_receive(self):
        """"Received" packet ID must be marked as received."""
        window = ReceiverWindow(100, 1)

        packet_id = rnd.choice(list(window))

        window.receive(packet_id=packet_id)
        assert window.is_received(packet_id=packet_id)
        assert not window.is_skipped(packet_id=packet_id)

    def test_receive_skipped(self):
        """When "skipped" packet ID is received it becomes "received"."""
        window = ReceiverWindow(100, 1)

        expected_starting_packet_id = list(window)[50]
        expected_skipped_packet = list(window)[49]

        window.move(packet_id=expected_starting_packet_id)
        assert window.start == expected_starting_packet_id
        assert window.is_skipped(packet_id=expected_skipped_packet)
        window.receive(packet_id=expected_skipped_packet)
        assert not window.is_skipped(packet_id=expected_skipped_packet)

    def test_receive_unknown_id(self):
        """When unknown ID is received - an exception is raised."""
        window = ReceiverWindow(100, 1)

        unknown_id = next_packet_id(window.end)
        with pytest.raises(UnknownID):
            window.receive(unknown_id)

    def test_skipped_packets(self):
        """When window is moved - unreceived packet IDs become "skipped"."""
        window = ReceiverWindow(100, 1)

        new_starting_packet_id = list(window)[10]
        expected_skipped_packet_ids = list(window)[:10]
        window.move(new_starting_packet_id)

        assert all(
            window.is_skipped(packet_id)
            for packet_id in expected_skipped_packet_ids
        )
