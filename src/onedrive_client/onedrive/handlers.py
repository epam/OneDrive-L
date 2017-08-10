""" Processing data
"""

from json import dumps

import dbus
import dbus.service
import dbus.glib


class DataHandler(object):
    """
    Consumer for OneDrive
    Receives remote data
    """

    def __init__(self, source):
        """
        Init a specific handler
        :param source: an object that provides
        interface for processing data
        """
        self.source = source

    def receive(self, data):
        """
        Invokes by service when data comes
        :param data: raw data
        :return:
        """
        self.source.process(data)


class DBusHandler(dbus.service.Object):
    """ Dbus data handler
    """
    dbus_name = 'onedrive.client'
    dbus_topic = '/onedrive/monitor/event'

    def __init__(self):
        """
        Initialize dbus service
        """
        self.bn = dbus.service.BusName(DBusHandler.dbus_name,
                                       bus=dbus.SessionBus())
        super(DBusHandler, self).__init__(self.bn, DBusHandler.dbus_topic)

    def process(self, data):
        """
        The data processor
        :param data: raw data
        :return:
        """
        print('Processing data ...')
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
        """
        Handle new items
        :param data: str, json dumps
        :return:
        """
        print('Event on_created ...')

    @dbus.service.signal('onedrive.monitor.event')
    def on_modified(self, data):
        """
        Handle modified items
        :param data: str, json dumps
        :return:
        """
        print('Event on_modified ...')

    @dbus.service.signal('onedrive.monitor.event')
    def on_deleted(self, data):
        """
        Handle deleted items
        :param data: str, json dumps
        :return:
        """
        print('Event on_deleted ...')
