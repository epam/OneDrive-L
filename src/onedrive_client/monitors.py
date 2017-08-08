from time import sleep
import json


class OneDriveMonitor(object):
    def __init__(self, service):
        self.service = service
        self._run = False
        self._timeout = 5
        self.__subscribers = set()

    def register(self, subscriber):
        self.__subscribers.add(subscriber)

    def unregister(self, subscriber):
        self.__subscribers.discard(subscriber)

    def run(self):
        print "Starting OneDrive monitor ..."
        self._run = True
        while self._run:
            items = self.service.get_changes()
            for item in items:
                self.dispatch(json.dumps(item.to_dict()))

            sleep(self._timeout)

    def stop(self):
        self._run = False

    def get_subscribers(self):
        return self.__subscribers

    def dispatch(self, data):
        for subscriber in self.get_subscribers():
            subscriber.receive(data)
