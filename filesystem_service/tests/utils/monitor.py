"""
Provides useful functions for filesystem monitor tests
"""

import collections
from multiprocessing import Process
from time import sleep

from filesystem_service.monitor import Event, FileSystemMonitor


InotifyEvent = collections.namedtuple('_INOTIFY_EVENT',
                                      ['wd', 'mask', 'cookie', 'len'])


# pylint: disable=dangerous-default-value
# pylint: disable=too-few-public-methods
class Subscriber(object):
    """
    Subscriber emulator
    """

    def __init__(self, events=[]):
        self.events = events

    def update(self, event):
        """
        :param event: inotify event
        add events to shared list variable
        """

        self.events.append(event)


class SecondSubscriber(object):
    """
    Subscriber emulator
    """

    def __init__(self, events=[]):
        self.events = events

    def update(self, event):
        """
        :param event: inotify event
        add events to shared list variable
        """

        self.events.append(event)


def get_monitor_instance(folder='/test', subscribers=[]):
    """
    :param folder: folder to be watched
    :param subscribers: list of subscriber instances
    :return: an instance of FileSystemMonitor
    """

    monitor = FileSystemMonitor(folder)
    for subscriber in subscribers:
        monitor.subscribe(subscriber)

    return monitor


def gen_event_object():
    """
    :return: an instance of Event
    """

    i_event = (InotifyEvent(wd=1, mask=8, cookie=0, len=16),
               ['IN_CLOSE_WRITE', 'IN_ACCESS'], b'/tmp/onedrive',
               b'test')

    return Event(i_event)


def start_monitor_process(monitor):
    """
    :param monitor: an instance of monitor
    Starts monitor in its own process in the current thread
    """

    process = Process(target=monitor.monitor)
    process.start()
    sleep(0.1)

    return process
