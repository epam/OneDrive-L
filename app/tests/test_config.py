"""
Tests for the config module
"""

import os
from tempfile import mkstemp

from onedrive_client.utils.config import config_load
from onedrive_client.utils.errors import OneDriveConfigException
import pytest

_BAD_FILE_PATH = mkstemp()[1]
_FILE_PATH = mkstemp()[1]
_BAD_CONTENT = ':'
_CONTENT = 'parameter: test'


# pylint: disable=no-self-use
class TestConfigLoad(object):
    """
    Test class for the load functionality
    """

    def setup_class(self):
        """
        Write two temporary files for the tests
        """

        with open(_BAD_FILE_PATH, 'w') as tmpfile:
            tmpfile.write(_BAD_CONTENT)

        with open(_FILE_PATH, 'w') as tmpfile:
            tmpfile.write(_CONTENT)

    def teardown_class(self):
        """
        Remove temporary files
        """

        for path in (_FILE_PATH, _BAD_FILE_PATH):
            if os.path.exists(path):
                os.remove(path)

    def testbad_file(self):
        """
        Verify load config with malformed file
        """

        with pytest.raises(OneDriveConfigException):
            config_load(_BAD_FILE_PATH)

    def test_bad_path(self):
        """
        Verify load config with fake path
        """

        with pytest.raises(OneDriveConfigException):
            config_load('/path/to/nothing')

    def test_content(self):
        """
        Test the content of a loaded file
        """

        content = config_load(_FILE_PATH)

        assert content.get('parameter', 0) == 'test', 'Wrong file content'
