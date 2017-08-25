"""
Provides functionality to monitor local filesystem changes
"""

import os

import inotify.adapters


class FileSystemMonitor(object):
    """
    Monitor local filesystem changes and inform subscribers
    """

    def __init__(self, folder):
        """
        :param folder: folder to be watched. Type: string
        """

        self._root_folder = folder.encode()
        self._exclude_folders = set()
        self._subscribers = set()
        self._notifier = inotify.adapters.Inotify()

    @property
    def subscribers(self):
        """
        :return: List of subscribers
        """

        return self._subscribers

    def subscribe(self, subs):
        """
        Register new subscriber
        :param subs: an instance of subscriber
        :return:
        """

        self._subscribers.add(subs)

    def unsubscribe(self, subs):
        """
        Remove subscriber
        :param subs: an instance of subscriber
        :return:
        """

        self._subscribers.remove(subs)

    def add_exclude_folder(self, folder):
        """
        :param folder:full path to folder. Type: string
        :return:
        """

        self._exclude_folders.add(folder.encode())

    def __gen_watch_list(self):
        """
        :return: list of directoried to watch without excludes
        """

        return [res[0] for res in os.walk(self._root_folder)
                if res[0] not in self._exclude_folders]

    def __add_watch(self, folder):
        """
        :param folder: full path to folder to be watched. Type: string
        :return:
        """

        self._notifier.add_watch(folder.encode())

    def __remove_watch(self, folder):
        """
        :param folder: full path to folder to be removed from watch list.
        Type: string
        :return:
        """

        self._notifier.remove_watch(folder.encode())

    def monitor(self):
        """
        Notify subscribers about filesystem events
        :return:
        """

        for folder in self.__gen_watch_list():
            self._notifier.add_watch(folder)

        for event in self._notifier.event_gen():
            if event:
                for subscriber in self._subscribers:
                    file_object = Event(event)
                    subscriber.update(file_object)

                    # Removing a watch on folder 'cause it was deleted
                    if hasattr(file_object, 'IN_DELETE'):
                        self.__remove_watch(file_object.file_path)

                    # Adding a watch on folder 'cause we're being recursive
                    if hasattr(file_object, 'IN_CREATE') and \
                            os.path.isdir(file_object.file_path):
                        self.__add_watch(file_object.file_path)


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
