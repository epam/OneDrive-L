"""
Provides useful functions for filesystem monitor tests
"""

import collections
from multiprocessing import Manager, Process
import os
from time import sleep

from filesystem_service.monitor import Event, FileSystemMonitor

from .consts import SUBDIR_FPATH, SUBDIR_PATH


InotifyEvent = collections.namedtuple('_INOTIFY_EVENT',
                                      ['wd', 'mask', 'cookie', 'len'])
EVENTS = Manager().list()
SEVENTS = Manager().list()


# pylint: disable=too-few-public-methods
class Subscriber(object):
    """
    Subscriber emulator
    """

    @staticmethod
    def update(event):
        """
        :param event: inotify event
        add events to shared list variable
        """

        EVENTS.append(event)


class SecondSubscriber(object):
    """
    Subscriber emulator
    """

    @staticmethod
    def update(event):
        """
        :param event: inotify event
        add events to shared list variable
        """

        SEVENTS.append(event)


# pylint: disable=dangerous-default-value
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


def gen_events_list(monitor):
    """
    :param monitor: an instance of monitor
    Fills shared variable with events
    """

    process = start_monitor_process(monitor)
    os.system('mkdir -p {}'.format(SUBDIR_PATH))
    sleep(1)
    os.system('touch {}'.format(SUBDIR_FPATH))
    sleep(1)
    os.system('cat {}'.format(SUBDIR_FPATH))
    sleep(1)
    os.system('rm -rf {}'.format(SUBDIR_PATH))
    sleep(1)
    process.terminate()
