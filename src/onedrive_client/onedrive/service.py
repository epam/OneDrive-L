""" Provides service to interact with remote API
"""


class OneDriveService(object):
    """
    Provides access to the OneDrive API
    """

    def __init__(self, client, token=None):
        self.token = token
        self.root_path = 'root'
        self.client = client

    def set_root_path(self, name):
        """
        Set current directory
        :param name: str, root dir
        :return:
        """
        self.root_path = name

    def list_drives(self):
        """ Gets available drives
        """
        pass

    def get_drive(self, drive_id):
        """
        Get metadata for a drive
        :param drive_id:
        :return:
        """
        pass

    def get_item(self, item_id):
        """
        Get metadata for a OneDrive item
        :param item_id:
        :return:
        """
        pass

    def copy_item(self, item_id, name=None):
        """
        Copy an Item on OneDrive
        :param item_id:
        :param name:
        :return:
        """
        pass

    def move_item(self, item_id, path):
        """
        Move an item on OneDrive
        :param item_id:
        :param path:
        :return:
        """
        pass

    def delete_item(self, item_id):
        """
        Delete an Item in OneDrive
        :param item_id:
        :return:
        """
        pass

    def create_folder(self, parent_id, name):
        """
        Create a new folder in OneDrive
        :param parent_id:
        :param name:
        :return:
        """
        pass

    def download(self, item_id):
        """
        Download a OneDrive Item contents
        :param item_id:
        :return:
        """
        pass

    def simple_upload(self, parent_id, name, content):
        """
        Simple item upload to OneDrive
        :param parent_id:
        :param name:
        :param content:
        :return:
        """
        pass

    def get_changes(self):
        """
        Returns last changes from OneDrive
        :return: list
        """
        items = self.client.item(id=self.root_path).delta(self.token).get()
        self.token = items.token

        return items
