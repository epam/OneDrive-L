"""
Test script for daemonizing
"""

from sys import argv
from time import sleep

from onedrive_client.utils import daemon


def main():
    """
    Dummy function
    """

    while True:
        sleep(5)


# pylint: disable=invalid-name
daemon = daemon.Daemon(app='testapp', pid=argv[2], action=main)
if argv[1] == 'start':
    exit(daemon.start())
elif argv[1] == 'stop':
    exit(daemon.stop())
elif argv[1] == 'restart':
    exit(daemon.restart())
elif argv[1] == 'try-restart':
    exit(daemon.try_restart())
elif argv[1] == 'status':
    exit(daemon.status())
