"""
Module with unittests for the filesystem monitor
"""
# pylint: disable=protected-access

import os
import unittest

from .utils.consts import EXCLUDE_FOLDER, FOLDER, TEST_FILE, TEST_SUBDIR
from .utils.monitor import EVENTS, gen_event_object, gen_events_list,\
    get_monitor_instance, Subscriber


class FileSystemMonitorTest(unittest.TestCase):
    """
    Tests for the filesystem monitor
    """

    def setUp(self):
        """
        Create instance of a monitor
        """

        self.monitor = get_monitor_instance()
        self.sub1 = Subscriber()
        self.sub2 = Subscriber()

    def test_add_subscriber(self):
        """
        Add subscriber to the list of subscribers. Check if it's not empty.
        """

        self.monitor.subscribe(self.sub1)
        self.assertTrue(self.monitor.subscribers,
                        'List of subscriber is empty')

    def test_add_several_subscribers(self):
        """
        Add two subscribers to the list of subscribers. Check if number of
        subscribers is correct.
        """

        self.monitor.subscribe(self.sub1)
        self.monitor.subscribe(self.sub2)
        self.assertEqual(len(self.monitor.subscribers), 2,
                         'Wrong number of subscribers')

    def test_add_identical_subscribers(self):
        """
        Add two subscribers to the list of subscribers. Check if number of
        subscribers is correct.
        """

        self.monitor.subscribe(self.sub1)
        self.monitor.subscribe(self.sub1)
        self.assertEqual(len(self.monitor.subscribers), 1,
                         'Wrong number of subscribers')

    def test_remove_subscriber(self):
        """
        Add, remove subscriber. Verify that the list of subscribers is empty.
        """

        self.monitor.subscribe(self.sub1)
        self.monitor.unsubscribe(self.sub1)
        self.assertFalse(self.monitor.subscribers,
                         'List of subscriber is not empty')

    def test_add_exclude(self):
        """
        Add folder to exclude list. Verify that the list of excludes
        contains valid folder.
        """

        self.monitor.add_exclude_folder(EXCLUDE_FOLDER)
        self.assertTrue(self.monitor._exclude_folders,
                        'List of excludes is empty')

        self.assertEqual(len(self.monitor._exclude_folders), 1,
                         'Lack of excludes in exclude list')

        self.assertEqual(list(self.monitor._exclude_folders)[0],
                         EXCLUDE_FOLDER.encode(),)

    def test_add_folder(self):
        """
        Add a folder for monitoring. Verify that the folder is correctly set.
        """

        self.assertEqual(b'/test', self.monitor._root_folder)


class EventTest(unittest.TestCase):
    """
    Tests for the filesystem event class
    """

    def __init__(self, *args, **kwargs):
        super(EventTest, self).__init__(*args, **kwargs)
        self.event = gen_event_object()

    def test_event_hasattrs(self):
        """
        Verify that all event types are among event object attributes
        """

        for attr in ['IN_CLOSE_WRITE', 'IN_ACCESS']:
            self.assertTrue(hasattr(self.event, attr),
                            'Missing event attributes')

    def test_event_attrs(self):
        """
        Verify event object attribute values
        """

        self.assertEqual(self.event.cookie, 0, 'Wrong attribute value')

        self.assertEqual(self.event.path, '/tmp/onedrive',
                         'Wrong attribute value')

        self.assertEqual(self.event.filename, 'test', 'Wrong attribute value')


class MonitorTest(unittest.TestCase):
    """
    Tests for the filesystem event's monitoring functionality
    """

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(FOLDER):
            os.mkdir(FOLDER)
        gen_events_list(get_monitor_instance(FOLDER, Subscriber()))

    def test_empty_events(self):
        """
        Check if events list is not empty
        """

        self.assertTrue(EVENTS, 'List of events is empty')

    def test_event_create(self):
        """
        Test create events
        """

        create_events = []
        for event in EVENTS:
            if hasattr(event, 'IN_CREATE'):
                create_events.append(event)

        self.assertTrue(create_events, 'Create events were not found')

        files_created = [event.filename for event in create_events]
        self.assertEqual(len(files_created), 2,
                         'Wrong number of create events')
        self.assertTrue(TEST_SUBDIR in files_created,
                        'Create event for {} is missing'.format(TEST_SUBDIR))
        self.assertTrue(TEST_FILE in files_created,
                        'Create event for {} is missing'.format(TEST_FILE))

    def test_event_delete(self):
        """
        Test delete events
        """

        delete_event = None
        for event in EVENTS:
            if hasattr(event, 'IN_DELETE') and event.filename == TEST_SUBDIR:
                delete_event = event
                break

        self.assertIsNotNone(delete_event, 'Delete events were not found')

        self.assertEqual(delete_event.filename, TEST_SUBDIR,
                         'Delete event for {} is missing'.format(TEST_SUBDIR))
