""" Processing data
"""


class DataHandler(object):  # pylint: disable=too-few-public-methods
    """
    Consumer for OneDrive
    Receives remote data
    """

    def __init__(self, source):
        """
        Init a specific handler
        :param source: an object that provides
        interface for processing data
        """
        self.source = source

    def receive(self, data):
        """
        Invokes by service when data comes
        :param data: raw data
        :return:
        """
        self.source.process(data)
