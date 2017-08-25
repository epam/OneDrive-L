"""
Module with unittests for the filesystem monitor
"""
# pylint: disable=protected-access

import collections
import unittest

from filesystem_service import monitor

InotifyEvent = collections.namedtuple('_INOTIFY_EVENT',
                                      ['wd', 'mask', 'cookie', 'len'])


class FileSystemMonitorTest(unittest.TestCase):
    """
    Tests for the filesystem monitor
    """

    def setUp(self):
        """
        Create instance of a monitor
        """

        self.monitor = monitor.FileSystemMonitor(folder='/test_dir')

    def test_add_subscriber(self):
        """
        Add subscriber to the list of subscribers. Check if it's not empty.
        """

        self.monitor.subscribe('subscriber')
        self.assertTrue(self.monitor.subscribers,
                        'List of subscriber is empty')

    def test_add_several_subscribers(self):
        """
        Add two subscribers to the list of subscribers. Check if number of
        subscribers is correct.
        """

        self.monitor.subscribe('subscriber1')
        self.monitor.subscribe('subscriber2')
        self.assertEqual(len(self.monitor.subscribers), 2,
                         'Wrong number of subscribers')

    def test_remove_subscriber(self):
        """
        Add, remove subscriber. Verify that the list of subscribers is empty.
        """

        self.monitor.subscribe('subscriber')
        self.monitor.unsubscribe('subscriber')
        self.assertFalse(self.monitor.subscribers,
                         'List of subscriber is not empty')

    def test_add_exclude(self):
        """
        Add folder to exclude list. Verify that the list of excludes
        contains valid folder.
        """

        self.monitor.add_exclude_folder('/test_dir/exclude')
        self.assertTrue(self.monitor._exclude_folders,
                        'List of excludes is empty')

        self.assertEqual(len(self.monitor._exclude_folders), 1,
                         'Lack of excludes in exclude list')

        self.assertEqual(list(self.monitor._exclude_folders)[0],
                         b'/test_dir/exclude',)

    def test_add_folder(self):
        """
        Add a folder for monitoring. Verify that the folder is correctly set.
        """

        self.assertEqual(b'/test_dir', self.monitor._root_folder)


class EventTest(unittest.TestCase):
    """
    Tests for the filesystem event class
    """

    def __init__(self, *args, **kwargs):
        super(EventTest, self).__init__(*args, **kwargs)
        self.i_event = (InotifyEvent(wd=1, mask=8, cookie=0, len=16),
                        ['IN_CLOSE_WRITE', 'IN_ACCESS'], b'/tmp/onedrive',
                        b'test')
        self.event = monitor.Event(self.i_event)

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
