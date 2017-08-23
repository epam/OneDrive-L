import unittest

from filesystem_service import monitor


class FileSystemMonitorTest(unittest.TestCase):

    def setUp(self):
        self.monitor = monitor.FileSystemMonitor()

    def test_add_subscriber(self):
        self.monitor.register_subscriber('subscriber')
        self.assertTrue(self.monitor.subscribers, 'List of subscriber is empty')

    def test_add_several_subscribers(self):
        self.monitor.register_subscriber('subscriber1')
        self.monitor.register_subscriber('subscriber2')
        self.assertEqual(len(self.monitor.subscribers), 2, 'Wrong number of subscribers')

    def test_remove_subscriber(self):
        self.monitor.register_subscriber('subscriber')
        self.monitor.unregister_subscriber('subscriber')
        self.assertFalse(self.monitor.subscribers, 'List of subscriber is not empty')

    def test_add_folder(self):
        self.monitor.folder = '/test_dir'
        self.assertEqual(b'/test_dir', self.monitor.folder)

    def test_add_folder_bytestring(self):
        self.assertRaises(AttributeError, self.monitor.folder, b'/test_dir')




