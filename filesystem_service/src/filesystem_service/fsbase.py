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
        self._exclude_folder = set()
        self._process = None
        self._subscribers = set()
        self.notifier = inotify.adapters.Inotify()

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
    def exclude_folder(self):
        """
        :return: list of folders to be excluded from monitoring
        """

        return self._exclude_folder

    def add_exclude_folder(self, folder):
        """
        :param folder:full path to folder. Type: string
        :return:
        """

        self._exclude_folder.add(folder.encode())

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

    def gen_watch_list(self):
        """
        :return: list of directoried to watch without excludes
        """

        return [res[0]for res in os.walk(self.folder)
                if res[0] not in self.exclude_folder]

    def notify(self):
        """
        Notify subscribers about filesystem events
        :return:
        """

        for folder in self.gen_watch_list():
            self.notifier.add_watch(folder)

        for event in self.notifier.event_gen():
            if event is not None:
                for subscriber in self._subscribers:
                    file_object = Event(event)
                    subscriber.update(file_object)


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class Event(object):
    """
    Object of local filesystem event
    """

    def __init__(self, event):
        """
        :param event:  inotify event
        """

        (header, type_names, path, filename) = event
        self.cookie = header.cookie
        self.path = path.decode('utf-8')
        self.filename = filename.decode('utf-8')
        self.file_path = os.path.join(self.path, self.filename)
        for i_event in type_names:
            if not hasattr(self, i_event):
                setattr(self, i_event, True)
