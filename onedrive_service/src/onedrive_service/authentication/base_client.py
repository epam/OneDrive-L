""" Base class for OneDrive clients.
"""

import os
import onedrivesdk


class BaseOneDriveClient(onedrivesdk.OneDriveClient):
    """ Base class for OneDrive API clients.
    """

    @staticmethod
    def check_saved_session_exists() -> bool:
        """ Returns 'True' if saved sessions exists.
        """

        current_path = os.getcwd()
        session_path = os.path.join(current_path, 'session.pickle')
        return os.path.exists(session_path)
