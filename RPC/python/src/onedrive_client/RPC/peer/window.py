"""Provides implementation of sliding-window algorithm implementation."""
import collections
import itertools as it
import random as rnd

import expiringdict
import mmh3


class WindowError(Exception):
    """Base window-related exception."""
    pass


class UnknownID(WindowError):
    """The packet ID does not belong to the window."""
    pass


def next_packet_id(packet_id: int):
    """Calculates next packet ID based on given 'packet_id'."""
    # The bitwise operation is for converting
    # the number from signed to unsigned.
    # pylint: disable=no-member
    return mmh3.hash(packet_id.to_bytes(4, 'big', signed=False)) & 0xffffffff


def id_range(start, size: int = None):
    """Range of successive packet IDs."""
    previous = start
    yield start
    if size is None:
        iterator = it.repeat(1)
    else:
        iterator = range(size - 1)

    for _ in iterator:
        previous = next_packet_id(previous)
        yield previous


_RANDOM = rnd.SystemRandom()


class BaseWindow:
    """Base window class. Implements common methods."""
    N_PREVIOUS_IDS = 1000

    def __init__(self, size, start=None):
        self.__size = size
        self.__previous_ids = collections.deque(maxlen=self.N_PREVIOUS_IDS)
        self.__window = collections.deque(maxlen=len(self))
        if start is not None:
            self.__window.extend(list(id_range(start, self.__size)))

    @property
    def start(self):
        """Start ID."""
        if len(self.__window) > 0:
            return self.__window[0]
        return None

    def move(self, packet_id: int):
        """Move window forward to 'packet_id'.

        After this operation the window's start becomes equal to 'packet_id'.
        """
        if packet_id == self.start:
            return

        if packet_id in self.__previous_ids:
            raise UnknownID(packet_id)

        if self.start is None:
            self.__window.extend(id_range(start=packet_id, size=len(self)))
            return

        previous_ids = []
        for packet_id_ in id_range(self.start, len(self) * 2):
            if packet_id_ == packet_id:
                self.__window.clear()
                self.__window.extend(id_range(start=packet_id, size=len(self)))
                self.__previous_ids.extend(previous_ids)
                break
            else:
                previous_ids.append(packet_id_)
        else:
            raise UnknownID(packet_id)

    @property
    def end(self):
        """End packet ID."""
        if len(self.__window) > 0:
            return self.__window[-1]
        return None

    def __contains__(self, item):
        return item in self.__window

    def __iter__(self):
        return iter(self.__window)

    def __len__(self):
        return self.__size


class SenderWindow(BaseWindow):
    """Sliding-window of the sender side."""
    def __init__(self, size, start=None):
        if start is None:
            start = _RANDOM.randrange(2 ** 32)
        super().__init__(size=size, start=start)

        self.__cleared = set()
        self.__sent = set()

    def clear(self, packet_id):
        """"Clear" packet ID.

        Mark packet as a packet ID which delivery is in satisfactory state.
        """
        if packet_id not in self or packet_id not in self.__sent:
            raise UnknownID(packet_id)

        self.__cleared.add(packet_id)

        if packet_id == self.start:
            for packet_id_ in self:
                if packet_id_ in self.__cleared:
                    self.__cleared.discard(packet_id_)
                else:
                    self.move(packet_id_)
                    break

    def send(self, packet_id: int):
        """Mark the packet ID as sent."""
        if packet_id not in self:
            raise UnknownID(packet_id)
        elif packet_id in self.__cleared:
            raise UnknownID(packet_id)
        self.__sent.add(packet_id)

    def free_ids(self, count=None):
        """Return IDs from the window that are free to use in new packets."""
        n = 0
        for packet_id in self:
            if count is not None and n >= count:
                break
            if not (self.is_cleared(packet_id) or self.is_sent(packet_id)):
                yield packet_id
                n += 1

    def is_cleared(self, packet_id: int):
        """Whether the packet ID is "cleared"."""
        return packet_id in self.__cleared

    def is_sent(self, packet_id: int):
        """Whether the packet ID is sent."""
        return packet_id in self.__sent

    def move(self, packet_id: int):
        """Move window forward."""
        super().move(packet_id)
        self.__cleared &= set(self)


class ReceiverWindow(BaseWindow):
    """Sliding window of the receiver-side.

    Window start must be provided explicitly as it's only could be known
    when a packet from the remote peer is received. Otherwise it's ``None``.
    """
    MAX_SKIPPED_PACKETS = 100000
    MAX_SKIPPED_PACKET_AGE = 30

    def __init__(self, size, start=None):
        super().__init__(size=size, start=start)
        self.__skipped = expiringdict.ExpiringDict(
            max_len=self.MAX_SKIPPED_PACKETS,
            max_age_seconds=self.MAX_SKIPPED_PACKET_AGE
        )
        self.__received = set()

    def move(self, packet_id: int):
        """Move the window forward."""
        if packet_id == self.start:
            return

        old_start = self.start

        super().move(packet_id)

        if old_start is None:
            return

        for packet_id_ in id_range(old_start):
            if packet_id_ == self.start:
                break
            if packet_id_ not in self.__received:
                self.__skipped[packet_id_] = None

        self.__received &= set(self)

    def receive(self, packet_id: int):
        """Mark the packet ID as received."""
        if packet_id in self.__skipped:
            self.__skipped.pop(packet_id, None)
        elif packet_id in self:
            self.__received.add(packet_id)
        else:
            raise UnknownID(packet_id)

    def is_received(self, packet_id: int):
        """Whether the packet is received."""
        return packet_id in self.__received

    def is_skipped(self, packet_id: int):
        """Whether the packet was not received before the window was moved.

        Skipped packet IDs are packets that are "left-behind" and not received
        at the moment when the window is moved forward.
        """
        return packet_id in self.__skipped
