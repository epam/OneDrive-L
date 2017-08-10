""" Defines OneDrive client errors
"""


class OneDriveClientError(Exception):
    pass


class OneDriveMonitorError(OneDriveClientError):
    pass
