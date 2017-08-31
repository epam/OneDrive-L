"""
Test utility for demonizing
"""

import os
from time import sleep
import unittest

import psutil

THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))


class TestDaemon(unittest.TestCase):
    """
    Test common utility for demonizing
    """

    def __init__(self, *args, **kwargs):
        super(TestDaemon, self).__init__(*args, **kwargs)
        self.pidfile = '/tmp/testapp.pid'
        self.cmd = 'python3.6 %s/daemon_script.py %s %s'


class TestStart(TestDaemon):
    """
    Test daemon start functionality
    """

    def test_start(self):
        """
        Verifies that pidfile is created, process exists, pidfile is not empty.
        """

        result = os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(1)

        self.assertTrue(os.path.exists(self.pidfile),
                        'Pidfile has not been created')

        with open(self.pidfile) as pid_file:
            pid = pid_file.read().rstrip()

        self.assertTrue(pid, 'Pidfile is empty')

        self.assertTrue(psutil.pid_exists(int(pid)),
                        'Process with specified pid does not exist')

        self.assertEqual(result, 0, 'Wrong return code')

    def tearDown(self):
        """
        Test cleanup
        """

        os.system('kill `cat %s`' % self.pidfile)
        sleep(1)


class TestStop(TestDaemon):
    """
    Test daemon stop functionality
    """

    def setUp(self):
        """
        Start daemon process
        """

        os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(1)

    def test_stop(self):
        """
        Test daemon stop functionality. Verifies that pidfile is being removed,
        process does not exist.
        """

        with open(self.pidfile) as pid_file:
            pid = pid_file.read().rstrip()

        result = os.system(self.cmd % (THIS_FILE_PATH, 'stop', self.pidfile))
        sleep(1)

        self.assertEqual(result, 0, 'Wrong return code')

        self.assertFalse(psutil.pid_exists(int(pid)),
                         'Process with {0} pid still exists'.format(pid))

        self.assertFalse(os.path.exists(self.pidfile),
                         'Pidfile has not been removed')


class TestRestart(TestDaemon):
    """
    Test daemon restart functionality
    """

    def setUp(self):
        """
        Start daemon process
        """

        os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(1)

    def test_restart(self):
        """
        Verify that pidfile is created, process exists, pidfile is not empty.
        """

        result = os.system(self.cmd % (THIS_FILE_PATH, 'restart',
                                       self.pidfile))
        sleep(1)

        self.assertTrue(os.path.exists(self.pidfile),
                        'Pidfile has not been created')

        with open(self.pidfile) as pid_file:
            pid = pid_file.read().rstrip()

        self.assertTrue(pid, 'Pidfile is empty')

        self.assertTrue(psutil.pid_exists(int(pid)),
                        'Process with specified pid does not exist')

        self.assertEqual(result, 0, 'Wrong return code')

    def tearDown(self):
        """
        Test cleanup
        """

        os.system('kill `cat %s`' % self.pidfile)
        sleep(1)


class TestTryRestart(TestDaemon):
    """
    Test daemon try-restart functionality
    """

    # pylint: disable=invalid-name
    def test_try_restart_without_pidfile(self):
        """
        Verify that try-restart does not restart daemon if pidfile is absent
        """

        result = os.system(self.cmd % (THIS_FILE_PATH, 'try-restart',
                                       self.pidfile))

        self.assertEqual(result, 256, 'Wrong return code')

    def test_try_restart_with_fake_proc(self):
        """
        Verify that try-restart does not restart daemon with fake PID
        """

        with open(self.pidfile, 'w') as pid_file:
            pid_file.write('abc')
            pid_file.close()

        result = os.system(self.cmd % (THIS_FILE_PATH, 'try-restart',
                                       self.pidfile))

        self.assertEqual(result, 256, 'Wrong return code')

    def test_try_restart(self):
        """
        Verify that try-restart does restart for running process
        """

        os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(1)

        result = os.system(self.cmd % (THIS_FILE_PATH, 'try-restart',
                                       self.pidfile))

        self.assertEqual(result, 0, 'Wrong return code')

        os.system('kill `cat %s`' % self.pidfile)
        sleep(0.1)

    def tearDown(self):
        """
        Cleanup method
        """

        try:
            os.remove(self.pidfile)
        except FileNotFoundError:
            pass


class TestStatus(TestDaemon):
    """
    Test daemon try-restart functionality
    """

    def test_status_without_pidfile(self):
        """
        Test return code if pidfile is absent
        """

        result = os.system(self.cmd % (THIS_FILE_PATH, 'status', self.pidfile))

        self.assertEqual(result, 768, 'Wrong return code')

    def test_status_with_fake_proc(self):
        """
        Test return code with daemon with fake PID
        """

        with open(self.pidfile, 'w') as pid_file:
            pid_file.write('abc')
            pid_file.close()

        result = os.system(self.cmd % (THIS_FILE_PATH, 'status', self.pidfile))

        self.assertEqual(result, 256, 'Wrong return code')

        os.remove(self.pidfile)

    def test_status(self):
        """
        Test return code for running process
        """

        os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(1)

        result = os.system(self.cmd % (THIS_FILE_PATH, 'status', self.pidfile))

        self.assertEqual(result, 0, 'Wrong return code')

        os.system('kill `cat %s`' % self.pidfile)
        sleep(0.1)
