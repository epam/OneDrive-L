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
daemon = daemon.Daemon(app="testapp", pid=argv[2], action=main)
if argv[1] == 'start':
    daemon.start()
elif argv[1] == 'stop':
    daemon.stop()
if argv[1] == 'restart':
    daemon.restart()
