import dbus
import dbus.service
import dbus.glib

from pprint import pprint
from json import dumps


class DataHandler(object):
    def __init__(self, source):
        self.source = source

    def receive(self, data):
        self.source.process(data)


class DBusHandler(dbus.service.Object):
    dbus_name = 'onedrive.client'
    dbus_topic = '/onedrive/monitor/event'

    def __init__(self):
        self.bn = dbus.service.BusName(DBusHandler.dbus_name,bus=dbus.SessionBus())
        super(DBusHandler, self).__init__(self.bn, DBusHandler.dbus_topic)

    def process(self, data):
        print("Processing data ...")
        for item in data:
            # invokes a proper event
            if hasattr(item, 'deleted') and item.deleted is not None:
                event = self.on_deleted
            elif item.created_date_time == item.last_modified_date_time:
                event = self.on_created
            else:
                event = self.on_modified

            event(dumps(item.to_dict()))

    @dbus.service.signal('onedrive.monitor.event')
    def on_created(self, data):
        print("Event on_created ...")

    @dbus.service.signal('onedrive.monitor.event')
    def on_modified(self, data):
        print("Event on_modified ...")

    @dbus.service.signal('onedrive.monitor.event')
    def on_deleted(self, data):
        print("Event on_deleted ...")
