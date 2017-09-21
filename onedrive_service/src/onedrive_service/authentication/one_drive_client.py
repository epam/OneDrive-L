""" API client for OneDrive for personal use.
"""

import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

from .base_client import BaseOneDriveClient
from .session import Session


API_BASE_URL = 'https://api.onedrive.com/v1.0/'


class OneDriveClient(BaseOneDriveClient):
    """ API client for OneDrive for personal use.
    """

    def __init__(self, config: dict) -> None:
        """ Basic initialization.
        """

        self._config = config
        client_id = config['auth']['client_id']
        scopes = config['auth']['scopes']

        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(http_provider, client_id,
                                                 scopes, session_type=Session)

        super().__init__(API_BASE_URL, auth_provider, http_provider)

    def authenticate(self, client_secret=None,
                     redirect_uri='http://localhost:8080/', auth_code=None):
        """ Authenticate process for OneDrive for personal use.
        """

        if client_secret is None:
            client_secret = self._config['auth']['client_secret']

        if self.check_saved_session_exists():
            self.auth_provider.load_session()
        else:
            if auth_code is None:
                auth_url = self.auth_provider.get_auth_url(redirect_uri)
                auth_code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

            self.auth_provider.authenticate(auth_code, redirect_uri, client_secret)
            self.auth_provider.save_session()
