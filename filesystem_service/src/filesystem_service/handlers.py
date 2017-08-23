"""
Filesystem event handlers
"""

from json import dumps

import dbus
import dbus.glib
import dbus.service


IMP_EVENTS = ['IN_ATTRIB', 'IN_CLOSE_WRITE', 'IN_MOVED_TO', 'IN_MOVED_FROM',
              'IN_CREATE', 'IN_DELETE']


# pylint: disable=too-few-public-methods
class FilesystemEventHandler(object):
    """
    Filesystem event receiver
    """

    def __init__(self, source):
        """
        Init a specific handler
        :param source: an object that provides
        interface for processing data
        :return:
        """

        self.source = source

    def update(self, event):
        """
        Invokes by service when data comes
        :param event: filesystem event
        :return:
        """

        for i_event in IMP_EVENTS:
            if event.__dict__.get(i_event, False):
                self.source.event(dumps(event.__dict__))


# pylint: disable=too-few-public-methods
class FileSystemDbusHandler(dbus.service.Object):
    """ Dbus data handler
    """
    dbus_name = 'onedrive.client'
    dbus_topic = '/filesystem/monitor/event'

    def __init__(self):
        """
        Initialize dbus service
        """

        self.bus_name = dbus.service.BusName(FileSystemDbusHandler.dbus_name,
                                             bus=dbus.SessionBus())
        super(FileSystemDbusHandler, self).__init__(self.bus_name,
                                                    self.dbus_topic)

    @dbus.service.signal('filesystem.monitor.event')
    def event(self, data):  # pylint: disable=no-self-use
        """
        Handle new events
        :param data: str, json dumps
        :return:
        """

        return data
