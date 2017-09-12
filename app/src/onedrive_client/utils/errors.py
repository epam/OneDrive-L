"""
One-Drive client exceptions
"""


class OneDriveConfigException(Exception):
    """
    Catch exceptions working with configuration files
    """

    def __call__(self, message, *args, **kwargs):
        print(message)
