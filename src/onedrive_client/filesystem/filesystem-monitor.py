#!/usr/bin/python

import sys
#from pathlib import Path
import argparse

_FILESYSTEM_MONITOR = 'filesystem-monitor'
_FILESYSTEM_MONITOR_VERSION = '0.1.0'


def start_monitoring():
    """
    :return:
    """

    pass


def main():
    """
    :return:
    """

    parser = argparse.ArgumentParser(prog='filesystem-monitor',
                                     description='Starts monitoring of specified local folder(s)',
                                     epilog='OneDrive-L Filesystem Monitoring Service')
    parser.add_argument('-v', '--version', dest='version', action='version',
                        version="%(prog)s " + _FILESYSTEM_MONITOR_VERSION, help='Display version information')
    parser.add_argument('-p', '--path', dest='path', metavar='dir1', default=False, action='store',
                        help='Set path for monitoring')
    parser.add_argument('-e', '--exclude', dest='exclude', nargs='+', metavar='dir1,dir2',
                        default=[], action='store',
                        help='Exclude path or comma separated paths from monitored folder')
    args = parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
