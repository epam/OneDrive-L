"""Test OneDriveUtil functionality."""
# pylint: disable=protected-access
# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods

import mock

from onedrive_service.util import OneDriveUtil


class TestOneDriveUtil(object):
    """
    Test OneDriveUtil functionality
    """

    def test_get_full_path(self):
        """
        Test for _get_full_path
        :return:
        """
        client = mock.Mock()
        od_util = OneDriveUtil(client)

        relative_path = '/Docs'
        full_path = od_util._get_full_path(relative_path)
        assert full_path == '/drive/root:/Docs'

        relative_path = '/Docs/'
        full_path = od_util._get_full_path(relative_path)
        assert full_path == '/drive/root:/Docs/'

        relative_path = '/'
        full_path = od_util._get_full_path(relative_path)
        assert full_path == '/drive/root:/'

        relative_path = ''
        full_path = od_util._get_full_path(relative_path)
        assert full_path == '/drive/root:/'
