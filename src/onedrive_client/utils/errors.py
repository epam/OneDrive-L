""" Defines OneDrive client errors
"""


class OneDriveClientError(Exception):
    """ Base exception
    """
    pass


class OneDriveMonitorError(OneDriveClientError):
    """ Base monitor exception
    """
    pass
