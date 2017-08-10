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
        self.root_path = name

    def list_drives(self):
        pass

    def get_drive(self, drive_id):
        pass

    def get_item(self, item_id):
        pass

    def copy_item(self, item_id, name=None):
        pass

    def move_item(self, item_id, path):
        pass

    def delete_item(self, item_id):
        pass

    def create_folder(self, parent_id, name):
        pass

    def download(self, item_id):
        pass

    def simple_upload(self, parent_id, name, content):
        pass

    def get_changes(self):
        """
        Returns last changes from OneDrive
        :return: list
        """
        items = self.client.item(id=self.root_path).delta(self.token).get()
        self.token = items.token

        return items
