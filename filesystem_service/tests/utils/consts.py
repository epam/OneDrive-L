"""
Constants for filesystem monitor tests
"""

import os


FOLDER = '/tmp/test'
EXCLUDE_FOLDER = os.path.join(FOLDER, 'exclude')
TEST_FILE = 'testfile'
TEST_SUBDIR = 'subdir'
SUBDIR_PATH = os.path.join(FOLDER, TEST_SUBDIR)
SUBDIR_FPATH = os.path.join(SUBDIR_PATH, TEST_FILE)
