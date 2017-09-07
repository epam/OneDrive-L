"""
Module with demonizing instruments
"""

import os
import signal
from time import sleep

from daemonize import Daemonize
import psutil


class Daemon(Daemonize):
    """
    A generic daemon class.
    """

    def get_pid(self):
        """
        :return: daemon PID
        """

        try:
            with open(self.pid, 'r') as pidfile:
                pid = int(pidfile.read().strip())
        except IOError:
            pid = None

        return pid

    @staticmethod
    def get_process(pid):
        """
        :param pid: daemon PID
        :return: process object for the process if it exists
        """

        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            process = None

        return process

    def stop(self, force=True):
        """
        Stop the daemon process
        """

        pid = self.get_pid()
        if not pid:
            message = 'pidfile %s does not exist. '\
                      'Daemon not running?\n' % str(self.pid)
            print(message)
            # not an error in a restart
            if force:
                return 0
            return 1

        # Try killing the daemon process
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                sleep(0.1)
        except OSError as err:
            err_str = str(err.args)
            if err_str.find('No such process') > 0:
                if os.path.exists(self.pid):
                    os.remove(self.pid)
            else:
                print(err_str)
                return 1
        return 0

    def restart(self):
        """
        Restart the daemon
        """

        self.stop()
        self.start()

        return 0

    def try_restart(self):
        """
        Restart the daemon if process is running only
        """

        if self.stop(force=False):
            print('process is not running')
            return 1
        self.start()

        return 0

    def status(self):
        """
        Print any relevant status info, and return a status code, an integer:
        0        program is running or service is OK
        1	      program is dead and /var/run pid file exists
        2	      program is dead and /var/lock lock file exists
        3	      program is not running
        4	      program or service status is unknown
        5-99	  reserved for future LSB use
        100-149	  reserved for distribution use
        150-199	  reserved for application use
        200-254	  reserved
        """

        pid = self.get_pid()
        if not pid:
            print('pidfile %s does not exist', self.pid)
            return 3

        process = self.get_process(pid)
        if not process:
            print('process %s does not exist', str(pid))
            return 1

        if not process.is_running():
            print('process %s is not running', str(pid))
            return 3

        return 0
