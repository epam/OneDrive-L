import dbus
import dbus.service
import dbus.glib


class EventsHandler(object):
    handlers = ('on_created', 'on_modified', 'on_deleted')

    def __init__(self, source):
        for handler in self.handlers:
            assert hasattr(source, handler)

        self.source = source

    def receive(self, data):
        print "Processing data ..."
        self.source.on_created(data)
        self.source.on_modified(data)
        self.source.on_deleted(data)


class DBusEvents(dbus.service.Object):
    dbus_name = 'onedrive.client'
    dbus_topic = '/onedrive/monitor/event'

    def __init__(self):
        self.bn = dbus.service.BusName(DBusEvents.dbus_name, bus=dbus.SessionBus())
        super(DBusEvents, self).__init__(self.bn, DBusEvents.dbus_topic)

    @dbus.service.signal('onedrive.monitor.event')
    def on_created(self, data):
        print "Event on_created ..."
        print data

    @dbus.service.signal('onedrive.monitor.event')
    def on_modified(self, data):
        print "Event on_modified ..."
        print data

    @dbus.service.signal('onedrive.monitor.event')
    def on_deleted(self, data):
        print "Event on_deleted ..."
        print data
