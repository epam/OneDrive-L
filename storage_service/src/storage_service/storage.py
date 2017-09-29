"""
Provides storage instruments for synchronization state and for arbitrary data
"""


class DataBase(object):
    """
    Making the class attributes global
    """

    _shared_data = {}

    def __init__(self):
        self.__dict__ = self._shared_data


class Data(DataBase):
    """
    This class shares all its attributes among its various instances
    """

    def __init__(self, **kwargs):
        super(Data, self).__init__()
        self._shared_data.update(kwargs)

    def __str__(self):
        return str(self._shared_data)
