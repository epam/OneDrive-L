"""
Filesystem monitor exceptions
"""


class FilesystemMonitorException(Exception):
    """
    Catch filesystem service exceptions
    """

    def __call__(self, message, *args, **kwargs):
        print(message)
