"""
Provides functionality to monitor local filesystem changes
"""

import os

import inotify.adapters


class FileSystemMonitor(object):
    """
    Monitor local filesystem changes and inform subscribers
    """

    important_events = ('IN_CLOSE_WRITE', 'IN_CREATE', 'IN_DELETE',
                        'IN_MOVED_FROM', 'IN_MOVED_TO', 'IN_ATTRIB')

    def __init__(self, folder):
        """
        :param folder: folder to be watched. Type: string
        """

        self._root_folder = folder.encode()
        self._exclude_folders = set()
        self._subscribers = set()
        self._notifier = inotify.adapters.Inotify()
        self._move_from_cookies = dict()

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

        if subs not in self.subscribers:
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

        self._notifier.remove_watch(folder.encode(), superficial=True)

    @staticmethod
    def __is_event_important(event):
        """
        :param event: inotify event
        :return: True if any event type in inotify event is in
        FileSystemMonitor.important_events list
        """

        if any(e_type in FileSystemMonitor.important_events
               for e_type in event[1]):
            return True
        return False

    def __gen_events_on_move_to(self, move_to_event):
        """
        :param move_to_event: Event object generated for the MOVE_TO event type
        Notifies subscribers with two events: the first one is about to remove
        old file, the second is about to create new file
        """

        if move_to_event.cookie in self._move_from_cookies:
            move_from_event = self._move_from_cookies[move_to_event.cookie]
            move_from_event.in_delete = True
            self.__notify(move_from_event, move_to_event)

    def __notify(self, *events):
        """
        :param events: event object(s)
        Notifies all subscribers about events
        """

        for subscriber in self._subscribers:
            for event in events:
                subscriber.update(event)

    def monitor(self):
        """
        Notify subscribers about filesystem events
        :return:
        """

        for folder in self.__gen_watch_list():
            self._notifier.add_watch(folder)

        for event in self._notifier.event_gen():
            if event and FileSystemMonitor.__is_event_important(event):
                file_object = Event(event)

                # Saving event object which is being moved in dictionary to
                if hasattr(file_object, 'IN_MOVED_FROM'):
                    if file_object.cookie not in self._move_from_cookies:
                        self._move_from_cookies[file_object.cookie] = \
                            file_object
                        continue

                # Generating appropriate events on file movement
                if hasattr(file_object, 'IN_MOVED_TO'):
                    self.__gen_events_on_move_to(file_object)
                    continue

                # Removing a watch on folder 'cause it was deleted
                if hasattr(file_object, 'IN_DELETE'):
                    self.__remove_watch(file_object.file_path)

                # Adding a watch on folder 'cause we're being recursive
                if hasattr(file_object, 'IN_CREATE') and \
                        os.path.isdir(file_object.file_path):
                    self.__add_watch(file_object.file_path)

                self.__notify(file_object)


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
        self.is_dir = os.path.isdir(self.file_path)
        self.in_delete = True if hasattr(self, 'IN_DELETE') else False
