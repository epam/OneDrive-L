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

    def run(self):
        """
        Start monitor. Fetch remote data, feed subscribers
        :return:
        """
        print("Starting OneDrive monitor ...")
        self._run = True
        while self._run:
            items = self.service.get_changes()
            self.dispatch(items)
            sleep(self._timeout)

    def stop(self):
        """
        Stop monitor
        :return:
        """
        print("Stopping OneDrive monitor ...")
        self._run = False

    def get_subscribers(self):
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
        for subscriber in self.get_subscribers():
            subscriber.receive(data)
