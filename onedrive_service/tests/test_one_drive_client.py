""" Test OneDriveClient functionality.
"""
# pylint: disable=no-self-use
# pylint: disable=invalid-name

import unittest

import mock

from onedrive_service.authentication.one_drive_client import OneDriveClient


class TestOneDriveClient(unittest.TestCase):
    """ Test authenticate process for OneDrive for personal use.
    """

    def test_loading_saved_session(self):
        """ Check 'load_session' is called in auth process if saved session exists.
        """

        onedrive_client_module_path = 'onedrive_service.authentication.' \
                                      'one_drive_client'

        auth_provider_path = '{}.onedrivesdk.AuthProvider'.\
            format(onedrive_client_module_path)
        http_provider_path = '{}.onedrivesdk.HttpProvider'.\
            format(onedrive_client_module_path)
        check_session_method_name = '{}.OneDriveClient.' \
                                    'check_saved_session_exists'\
            .format(onedrive_client_module_path)

        test_config = {
            'auth': {
                'client_secret': 'test_client_secret',
                'client_id': 'test_client_id',
                'scopes': ['test', 'scopes', ]
            }
        }

        with mock.patch(check_session_method_name, return_value=True):
            with mock.patch(auth_provider_path):
                with mock.patch(http_provider_path):
                    client = OneDriveClient(test_config)
                    client.authenticate()

        client.auth_provider.load_session.assert_called_once()
        client.auth_provider.get_auth_url.assert_not_called()

    def test_sending_auth_request_to_server(self):
        """ Check 'get_auth_code' is called in auth process
        if saved session doesn't exist.
        """

        onedrive_client_module_path = 'onedrive_service.' \
                                      'authentication.one_drive_client'

        auth_provider_path = '{}.onedrivesdk.AuthProvider'.\
            format(onedrive_client_module_path)
        http_provider_path = '{}.onedrivesdk.HttpProvider'.\
            format(onedrive_client_module_path)
        auth_helper_path = '{}.onedrivesdk.helpers.' \
                           'GetAuthCodeServer.get_auth_code'.\
            format(onedrive_client_module_path)
        check_session_method_name = '{}.OneDriveClient.' \
                                    'check_saved_session_exists'.\
            format(onedrive_client_module_path)

        test_config = {
            'auth': {
                'client_secret': 'test_client_secret',
                'client_id': 'test_client_id',
                'scopes': ['test', 'scopes', ]
            }
        }

        with mock.patch(check_session_method_name, return_value=False):
            with mock.patch(auth_provider_path):
                with mock.patch(http_provider_path):
                    with mock.patch(auth_helper_path) as auth_helper_mock:
                        client = OneDriveClient(test_config)
                        client.authenticate()

        client.auth_provider.load_session.assert_not_called()
        client.auth_provider.get_auth_url.assert_called_once()
        client.auth_provider.save_session.assert_called_once()
        auth_helper_mock.assert_called_once()
