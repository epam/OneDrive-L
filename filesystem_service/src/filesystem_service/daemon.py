"""
Module with demonizing instruments
"""

import logging
from logging import handlers
import sys
import os
import signal
from time import sleep

from daemonize import Daemonize  # pylint: disable=import-error


class Daemon(Daemonize):
    """
    A generic daemon class.
    """

    def __init__(self, *args, **kwargs):
        super(Daemon, self).__init__(*args, **kwargs)
        if self.logger is None:
            self.set_logger()

    def set_logger(self):
        """
        Set logger if self.logger is None
        :return:
        """

        # Initialize logging.
        self.logger = logging.getLogger(self.app)
        self.logger.setLevel(logging.DEBUG)
        # Display log messages only on defined handlers.
        self.logger.propagate = False

        # Initialize syslog.
        # It will correctly work on OS X, Linux and FreeBSD.
        if sys.platform == "darwin":
            syslog_address = "/var/run/syslog"
        else:
            syslog_address = "/dev/log"

        # We will continue with syslog initialization only
        # if actually have such capabilities
        # on the machine we are running this.
        if os.path.exists(syslog_address):
            syslog = handlers.SysLogHandler(syslog_address)
            if self.verbose:
                syslog.setLevel(logging.DEBUG)
            else:
                syslog.setLevel(logging.INFO)
            # Try to mimic to normal syslog messages.
            formatter = logging.Formatter("%(asctime)s %(name)s: %(message)s",
                                          "%b %e %H:%M:%S")
            syslog.setFormatter(formatter)

            self.logger.addHandler(syslog)

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
            self.logger.warning(message, self.pid)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                sleep(0.1)
        except OSError as err:
            err_str = str(err.args)
            if err_str.find("No such process") > 0:
                if os.path.exists(self.pid):
                    os.remove(self.pid)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """

        self.logger.warning("Restarting daemon.")
        self.stop()
        self.start()
