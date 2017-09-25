""" Module contains OneDrive session representation.
"""

import os

from onedrivesdk import session


class Session(session.Session):
    """ OneDrive session representation.
    """

    def save_session(self, **save_session_kwargs):
        """ Save the current session.
        """

        # TODO: Need to rewrite for safety.
        super().save_session(**save_session_kwargs)

    @staticmethod
    def load_session(**load_session_kwargs):
        """ Load session.
        """

        # TODO: Need to rewrite for safety.
        return session.Session.load_session(**load_session_kwargs)

    @staticmethod
    def check_saved_session_exists():
        """ Returns 'True' if saved sessions exists.
        """

        # TODO: Need to rewrite for safety.

        current_path = os.getcwd()
        session_path = os.path.join(current_path, 'session.pickle')
        return os.path.exists(session_path)
