import dbus
import dbus.service
import dbus.glib


class EventsHandler(object):
    def __init__(self, source):
        self.source = source

    def receive(self, data):
        self.source.process(data)


class DBusEvents(dbus.service.Object):
    dbus_name = 'onedrive.client'
    dbus_topic = '/onedrive/monitor/event'

    def __init__(self):
        self.bn = dbus.service.BusName(DBusEvents.dbus_name, bus=dbus.SessionBus())
        super(DBusEvents, self).__init__(self.bn, DBusEvents.dbus_topic)

    def process(self, data):
        print "Processing data ..."
        self.source.on_created(data)
        self.source.on_modified(data)
        self.source.on_deleted(data)

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
