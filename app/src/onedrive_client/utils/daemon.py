"""
Module with demonizing instruments
"""

import os
import signal
import sys
from time import sleep

from daemonize import Daemonize


class Daemon(Daemonize):
    """
    A generic daemon class.
    """

    def stop(self):
        """
        Stop the daemon
        """

        # Get the pid from the pidfile
        try:
            with open(self.pid, 'r') as pidfile:
                pid = int(pidfile.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = 'pidfile %s does not exist. ' + \
                      'Daemon not running?\n'
            sys.stderr.write(message % self.pid)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                sleep(.1)
        except OSError as err:
            err_str = str(err.args)
            if err_str.find('No such process') > 0:
                if os.path.exists(self.pid):
                    os.remove(self.pid)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """

        self.stop()
        self.start()
