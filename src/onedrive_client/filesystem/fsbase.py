"""
Provides functionality to monitor local filesystem changes
"""

from multiprocessing import Process
import os

import inotify.adapters  # pylint: disable=import-error


class FileSystemMonitor(object):
    """
    Monitor local filesystem changes and inform subscribers
    """

    def __init__(self):
        self._folder = None
        self._process = None
        self._subscribers = set()

    @property
    def subscribers(self):
        """
        :return: List of subscribers
        """

        return self._subscribers

    def register_subscriber(self, subs):
        """
        Register new subscriber
        :param subs: an instance of subscriber
        :return:
        """

        self._subscribers.add(subs)

    def unregister_subscriber(self, subs):
        """
        Remove subscriber
        :param subs: an instance of subscriber
        :return:
        """

        self._subscribers.remove(subs)

    @property
    def folder(self):
        """
        :return: Monitored folder
        """

        return self._folder

    @folder.setter
    def folder(self, folder):
        """
        :param folder: full path to folder to be monitored. Type: string
        :return:
        """

        self._folder = folder.encode()

    def start(self):
        """
        Start process that generates filesystem events
        :return:
        """

        self._process = Process(target=self.notify)
        self._process.start()

    def stop(self):
        """
        Terminate filesystem event generator process
        :return:
        """

        if self._process:
            self._process.terminate()

    def notify(self):
        """
        Notify subscribers about filesystem events
        :return:
        """

        notifier = inotify.adapters.InotifyTree(self.folder)

        for event in notifier.event_gen():
            if event is not None:
                for subscriber in self._subscribers:
                    file_object = Event(event)
                    subscriber.update(file_object)


class Event(object):  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """
    Object of local filesystem event
    """

    def __init__(self, event):
        """
        :param event:  inotify event
        """

        (header, type_names, path, filename) = event
        self._event = event
        self.header_wd = header.wd
        self.header_mask = header.mask
        self.header_cookie = header.cookie
        self.header_len = header.len
        self.path = path.decode('utf-8')
        self.filename = filename.decode('utf-8')
        self.type_names = type_names

    @property
    def event(self):
        """
        :return: inotify event
        """

        return self._event

    @property
    def file_path(self):
        """
        :return: full path to file
        """

        return os.path.join(self.path, self.filename)