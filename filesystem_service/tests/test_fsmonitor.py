"""
Module with unittests for the filesystem monitor
"""
# pylint: disable=protected-access
# pylint: disable=anomalous-backslash-in-string

from multiprocessing import Manager
import os
import shutil
from time import sleep
import unittest

from .utils.consts import EXCLUDE_FOLDER, FOLDER, SUBDIR_COPY_PATH, \
    SUBDIR_FPATH, SUBDIR_PATH, TEST_FILE, TEST_SUBDIR
from .utils.monitor import gen_event_object, get_monitor_instance, \
    SecondSubscriber, start_monitor_process, Subscriber


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

    def setUp(self):
        self.event = gen_event_object()

    def test_event_hasattrs(self):
        """
        Verify that all event types are among event object attributes
        """

        for attr in ['IN_CLOSE_WRITE', 'IN_ACCESS', 'file_path', 'is_dir',
                     'in_delete']:
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

    def setUp(self):
        if os.path.exists(FOLDER):
            shutil.rmtree(FOLDER)
        os.makedirs(FOLDER)
        self.events = Manager().list()
        self.sevents = Manager().list()
        self.process = start_monitor_process(
            get_monitor_instance(FOLDER, [Subscriber(self.events),
                                          SecondSubscriber(self.sevents)]))

    def tearDown(self):
        self.process.terminate()
        sleep(0.1)

    def test_empty_events(self):
        """
        Check if events list is not empty
        """

        os.system('mkdir -p {}'.format(SUBDIR_PATH))
        sleep(1)

        self.assertTrue(self.events, 'List of events is empty for the '
                                     'first subscriber')
        self.assertTrue(self.sevents, 'List of events is empty for the '
                                      'second subscriber')

    def test_event_lists(self):
        """
        Check if event lists are equal between subscribers
        """

        os.system('mkdir -p {}'.format(SUBDIR_PATH))
        sleep(1)

        self.assertFalse(list(set(self.events) & set(self.sevents)),
                         'List of events for subscribers are not equal')

    def test_event_create(self):
        """
        Test handling of create events
        """

        os.system('mkdir -p {}'.format(SUBDIR_PATH))
        os.system('touch {}'.format(SUBDIR_FPATH))
        sleep(1)

        create_events = []
        for event in self.events:
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

    def test_event_copy(self):
        """
         Test handling of copy events
        """

        os.system('mkdir -p {}'.format(SUBDIR_PATH))
        os.system('touch {}'.format(SUBDIR_FPATH))
        os.system('\cp -R {} {}'.format(SUBDIR_PATH, SUBDIR_COPY_PATH))
        os.system('echo "test"  > {}'.format(os.path.join(SUBDIR_COPY_PATH,
                                                          TEST_FILE)))
        sleep(1)

        create_events = []
        read_event = False
        for event in self.events:
            if hasattr(event, 'IN_CREATE'):
                create_events.append(event)
            if event.filename == TEST_FILE and \
                    hasattr(event, 'IN_CLOSE_WRITE'):
                read_event = True

        files_created = [event.filename for event in create_events]

        self.assertTrue(create_events, 'Create events were not found')
        self.assertEqual(len(files_created), 3,
                         'Wrong number of create events')
        self.assertTrue(read_event,
                        '{} is not monitored after recursive copying'
                        .format(SUBDIR_COPY_PATH))

    def test_event_delete(self):
        """
        Test delete events
        """

        os.system('touch {}'.format(os.path.join(FOLDER, TEST_FILE)))
        os.system('rm -f {}'.format(os.path.join(FOLDER, TEST_FILE)))
        sleep(1)

        delete_event = None
        for event in self.events:
            if hasattr(event, 'IN_DELETE') and event.filename == TEST_FILE:
                delete_event = event
                break

        self.assertIsNotNone(delete_event, 'Delete event was not found')
        self.assertEqual(delete_event.filename, TEST_FILE,
                         'Delete event for {} is missing'
                         .format(os.path.join(FOLDER, TEST_FILE)))

    def test_event_move(self):
        """
        Test move events
        """

        mfilename = 'm' + TEST_FILE
        tfilepath = os.path.join(FOLDER, TEST_FILE)
        mfilepath = os.path.join(FOLDER, mfilename)
        os.system('touch {}'.format(tfilepath))
        os.system('mv {} {}'.format(tfilepath, mfilepath))
        sleep(1)

        moved_from_event = None
        moved_to_event = None
        for event in self.events:
            if hasattr(event, 'IN_MOVED_FROM') and event.filename == TEST_FILE:
                moved_from_event = event
            if hasattr(event, 'IN_MOVED_TO') and event.filename == mfilename:
                moved_to_event = event

        self.assertIsNotNone(moved_from_event,
                             'MOVED_FROM event was not found')
        self.assertIsNotNone(moved_to_event, 'MOVED_TO event was not found')
        self.assertEqual(moved_from_event.filename, TEST_FILE,
                         'Delete event for {} is missing'
                         .format(tfilepath))
        self.assertEqual(moved_to_event.filename, mfilename,
                         'Delete event for {} is missing'
                         .format(mfilepath))
        self.assertTrue(moved_from_event.in_delete,
                        'in_delete attribute of the MOVED_FROM event '
                        'was no set properly')
