"""
Module with unittests for the filesystem monitor
"""

import unittest

from filesystem_service import monitor


class FileSystemMonitorTest(unittest.TestCase):
    """
    Tests for the filesystem monitor
    """

    def setUp(self):
        """
        Create instance of a monitor
        """

        self.monitor = monitor.FileSystemMonitor()

    def test_add_subscriber(self):
        """
        Add subscriber to the list of subscribers. Check if it's not empty.
        """

        self.monitor.register_subscriber('subscriber')
        self.assertTrue(self.monitor.subscribers,
                        'List of subscriber is empty')

    def test_add_several_subscribers(self):
        """
        Add two subscribers to the list of subscribers. Check if number of
        subscribers is correct.
        """

        self.monitor.register_subscriber('subscriber1')
        self.monitor.register_subscriber('subscriber2')
        self.assertEqual(len(self.monitor.subscribers), 2,
                         'Wrong number of subscribers')

    def test_remove_subscriber(self):
        """
        Add, remove subscriber. Verify that the list of subscribers is empty.
        """

        self.monitor.register_subscriber('subscriber')
        self.monitor.unregister_subscriber('subscriber')
        self.assertFalse(self.monitor.subscribers,
                         'List of subscriber is not empty')

    def test_add_folder(self):
        """
        Add a folder for monitoring. Verify that the folder is correctly set.
        """

        self.monitor.folder = '/test_dir'
        self.assertEqual(b'/test_dir', self.monitor.folder)

    def test_add_folder_bytestring(self):
        """
        Verify that folder setter raises an exception if not string
        passed to it.
        """

        self.assertRaises(AttributeError, self.monitor.folder, b'/test_dir')
