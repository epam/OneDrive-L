"""Test OneDriveUtil functionality."""
# pylint: disable=protected-access
# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

import mock

from onedrive_service.util import OneDriveUtil
from onedrivesdk.options import HeaderOption


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

    def test_init_upload_session_header_0(self):
        """
        Test for _init_upload_session_header
        start from 0
        :return:
        """
        client = mock.Mock()
        od_util = OneDriveUtil(client)

        first_range = 0
        data_len = 100
        total = 1024

        expected_content = {'Content-Range': 'bytes 0-99/1024',
                            'Content-Length': 100}

        options = od_util._init_upload_session_header(first_range,
                                                      data_len, total)

        for option in options:
            assert isinstance(option, HeaderOption)
            assert option.key in expected_content
            assert option.value == expected_content[option.key]

    def test_init_upload_session_header_1000(self):
        """
        Test for _init_upload_session_header
        start from 1000
        :return:
        """
        client = mock.Mock()
        od_util = OneDriveUtil(client)

        first_range = 1000
        data_len = 24
        total = 1024

        expected_content = {'Content-Range': 'bytes 1000-1023/1024',
                            'Content-Length': 24}

        options = od_util._init_upload_session_header(first_range,
                                                      data_len, total)

        for option in options:
            assert isinstance(option, HeaderOption)
            assert option.key in expected_content
            assert option.value == expected_content[option.key]

    def test_init_upload_session_header_100(self):
        """
        Test for _init_upload_session_header
        start from 100
        :return:
        """
        client = mock.Mock()
        od_util = OneDriveUtil(client)

        first_range = 100
        data_len = 100
        total = 1024

        expected_content = {'Content-Range': 'bytes 100-199/1024',
                            'Content-Length': 100}

        options = od_util._init_upload_session_header(first_range,
                                                      data_len, total)

        for option in options:
            assert isinstance(option, HeaderOption)
            assert option.key in expected_content
            assert option.value == expected_content[option.key]
