""" Provides functionality to monitor remote changes
"""

from time import sleep


class OneDriveMonitor(object):
    """
    Monitor any changes and feed subscribers
    """

    def __init__(self, service):
        self.service = service
        self._run = False
        self._timeout = 5
        self.__subscribers = set()

    def register(self, subscriber):
        """
        Register any subscribers
        :param subscriber: an object that implements receive method
        :return:
        """
        self.__subscribers.add(subscriber)

    def unregister(self, subscriber):
        """
        Remove a particular subscriber
        :param subscriber: an instance of subscriber
        :return:
        """
        self.__subscribers.discard(subscriber)

    def monitor(self):
        """
        Start monitor. Fetch remote data, feed subscribers
        :return:
        """
        self._run = True
        while self._run:
            items = self.service.delta()
            self.dispatch(items)
            sleep(self._timeout)

    def shutdown(self):
        """
        Stop monitor
        :return:
        """
        self._run = False

    @property
    def subscribers(self):
        """
        Retrieves well-known list of subscribers
        :return: set
        """
        return self.__subscribers

    def dispatch(self, data):
        """
        Send raw data to subscribers
        :param data:
        :return:
        """
        for subscriber in self.subscribers:
            subscriber.receive(data)
