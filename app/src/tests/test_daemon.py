"""
Test utility for demonizing
"""

import os
from time import sleep
import unittest
from unittest.mock import Mock

import psutil

THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))


class TestDaemon(unittest.TestCase):
    """
    Test common utility for demonizing
    """

    def __init__(self, *args, **kwargs):
        super(TestDaemon, self).__init__(*args, **kwargs)
        self.pidfile = '/tmp/testapp.pid'
        self.test_method = Mock(return_value=True)
        self.cmd = 'python3.6 %s/daemon_script.py %s %s'


class TestDaemonStart(TestDaemon):
    """
    Test daemon start functionality
    """

    def test_daemon_start(self):
        """
        Verifies that pidfile is created, process exists, pidfile is not empty.
        :return:
        """

        os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(.1)

        self.assertTrue(os.path.exists(self.pidfile),
                        'Pidfile has not been created')

        with open(self.pidfile) as pid_file:
            pid = pid_file.read().rstrip()

        self.assertTrue(pid, 'Pidfile is empty')

        self.assertTrue(psutil.pid_exists(int(pid)),
                        'Process with specified pid does not exist')

    def tearDown(self):
        """
        :return:
        """

        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)


class TestDaemonStop(TestDaemon):
    """
    Test daemon stop functionality
    """

    def test_daemon_stop(self):
        """
        Test daemon stop functionality. Verifies that pidfile is being removed,
        process does not exist.
        :return:
        """

        os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(.1)

        with open(self.pidfile) as pid_file:
            pid = pid_file.read().rstrip()

        os.system(self.cmd % (THIS_FILE_PATH, 'stop', self.pidfile))
        sleep(.1)

        self.assertFalse(psutil.pid_exists(int(pid)),
                         'Process with {0} pid still exists'.format(pid))

        self.assertFalse(os.path.exists(self.pidfile),
                         'Pidfile has not been removed')


class TestDaemonRestart(TestDaemon):
    """
    Test daemon restart functionality
    """

    def test_daemon_restart(self):
        """
        Verifies that pidfile is created, process exists, pidfile is not empty.
        :return:
        """

        os.system(self.cmd % (THIS_FILE_PATH, 'start', self.pidfile))
        sleep(.1)

        os.system(self.cmd % (THIS_FILE_PATH, 'restart', self.pidfile))
        sleep(.1)

        self.assertTrue(os.path.exists(self.pidfile),
                        'Pidfile has not been created')

        with open(self.pidfile) as pid_file:
            pid = pid_file.read().rstrip()

        self.assertTrue(pid, 'Pidfile is empty')

        self.assertTrue(psutil.pid_exists(int(pid)),
                        'Process with specified pid does not exist')

    def tearDown(self):
        """
        :return:
        """

        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)
