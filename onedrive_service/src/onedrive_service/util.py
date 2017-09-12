""" Provides service to interact with remote API """
# pylint: disable=too-many-arguments
import json

import onedrivesdk


class OneDriveUtil(object):
    """
    Provides access to the OneDrive API
    """
    DRIVE_ROOT = '/drive/root'

    def __init__(self, client, token=None):
        self.token = token
        self.client = client

    def list_drives(self):
        """
        Gets available drives
        :return: list
        """
        return list(self.client.drives.get())

    def get_drive(self, drive_id):
        """
        Get metadata for a drive
        :param drive_id:
        :return:
        """
        return self.client.drives[drive_id].get()

    def get_items(self, item_id=None, item_path=None):
        """
        Get metadata for a OneDrive item
        :param item_id:
        :param item_path:
        :return:
        """
        return self.client.item(id=item_id, path=item_path).children.get()

    def get_item(self, item_id=None, item_path=None):
        """
        Get metadata for a OneDrive item
        :param item_id:
        :param item_path:
        :return:
        """
        return self.client.item(id=item_id, path=item_path).get()

    def copy_item(self, name=None, item_id=None,
                  item_path=None, parent_id=None, parent_path=None):
        """
        Copy an Item on OneDrive in async mode.
        :param name: str, new name
        :param item_id:
        :param item_path:
        :param parent_id:
        :param parent_path:
        :return: onedrive.AsyncOperationMonitor
        """
        item, ref = self._init_item_to_update(item_id, item_path,
                                              parent_id, parent_path)

        return item.copy(name=name, parent_reference=ref).post()

    def move_item(self, item_id=None, item_path=None,
                  parent_id=None, parent_path=None):
        """
        Move an item on OneDrive
        :param item_id: str, the item to update
        :param item_path: str
        :param parent_id: str, new parent id
        :param parent_path: str
        :return: onedrivesdk.Item
        """
        item, ref = self._init_item_to_update(item_id, item_path,
                                              parent_id, parent_path)

        updated_item = onedrivesdk.Item()
        updated_item.parent_reference = ref

        return item.update(updated_item)

    def delete_item(self, item_id=None, item_path=None):
        """
        Delete an Item in OneDrive
        :param item_id: str, item id to delete
        :param item_path: str, item path to delete
        :return:
        """
        item = self.client.item(id=item_id, path=item_path)
        item.delete()

    def create_folder(self, name, parent_id=None, parent_path=None):
        """
        Create a new folder in OneDrive
        :param name: str, new folder name
        :param parent_id: str, parent id
        :param parent_path: str, parent path
        :return:
        """
        folder_to_create = onedrivesdk.Item()
        folder_to_create.name = name
        folder_to_create.folder = onedrivesdk.Folder()

        item = self.client.item(id=parent_id, path=parent_path)

        return item.children.add(folder_to_create)

    def download(self, dst_file, item_id=None, item_path=None):
        """
        Download a OneDrive Item contents
        :param dst_file: str, local destination file
        :param item_id:
        :param item_path:
        :return:
        """
        item = self.client.item(id=item_id, path=item_path)
        item.download(dst_file)

    def simple_upload(self, name, src_file, parent_id=None, parent_path=None):
        """
        Simple item upload to OneDrive
        It's available for items with less than 4 MB of content
        :param name:
        :param src_file: str, path to file to upload
        :param parent_id:
        :param parent_path:
        :return: onedrivesdk.Item
        """
        item = self.client.item(id=parent_id, path=parent_path)

        return item.children[name].upload(src_file)

    def create_upload_session(self, name, parent_path):
        """
        Init an upload session
        :param name:
        :param parent_path:
        :return: onedrivesdk.UploadSession
        """
        item = onedrivesdk.ChunkedUploadSessionDescriptor()
        item.name = name

        return self.client.item(path=parent_path).create_session(item).post()

    def upload_session(self, upload_url, data, total, next_range=0):
        """
        Upload the file, or a portion of the file
        It is possible to upload the entire file in one fragment up to 60 MiB

        The recommended fragment size is between 5-10 MiB.
        :param upload_url: str, url to upload
        :param data: data to include in the body of the request
        :param total: integer, all fragments size in bytes
        :param next_range: integer,  next expected ranges value to determine
        where to start the next fragment
        :return: onedrivesdk.UploadSession
        """
        data_length = len(data)
        builder = onedrivesdk.ItemRequestBuilder(upload_url, self.client)

        req = builder.request()
        req.method = 'PUT'

        # init header options
        header_options = self._init_upload_session_header(next_range,
                                                          data_length, total)
        for option in header_options:
            req.append_option(option)

        # send chunk of data
        raw_response = req.send(data=data)
        entity = onedrivesdk.UploadSession(json.loads(raw_response.content))

        return entity

    def upload_session_status(self, upload_url):
        """
        Check the upload session status

        You can request the status of the file at any time,
        not just when the upload has failed.
        The server will respond with a list of missing
        byte ranges that need to be uploaded.
        :param upload_url:
        :return: onedrivesdk.UploadSession
        """
        builder = onedrivesdk.ItemRequestBuilder(upload_url, self.client)

        req = builder.request()
        req.method = 'GET'
        raw_response = json.loads(req.send().content)
        entity = onedrivesdk.UploadSession(raw_response)

        return entity

    def cancel_upload_session(self, upload_url):
        """
        Cancel an upload session
        :param upload_url: str
        :return:
        """
        req = onedrivesdk.ItemRequestBuilder(upload_url, self.client)
        return req.delete()

    def delta(self):
        """
        Returns last changes from OneDrive
        :return: list(onedrive.Item, ...)
        """
        items = self.client.item(path='/').delta(self.token).get()
        self.token = items.token

        return items

    @staticmethod
    def _init_upload_session_header(first_range, data_len, total):
        """
        Init header items for upload session request
        :param first_range: integer
        :param data_len: integer
        :param total: integer
        :return: list
        """
        header_items = []
        options = onedrivesdk.options

        if first_range + data_len > total:
            last_range = total - 1
        else:
            last_range = data_len - 1

        range_item = dict(first=first_range, last=first_range + last_range)
        content_range = {
            'range': '%(first)s-%(last)s' % range_item,
            'total': total
        }
        data_range = 'bytes %(range)s/%(total)s' % content_range

        header_items.append(options.HeaderOption('Content-Range', data_range))
        header_items.append(options.HeaderOption('Content-Length', data_len))

        return header_items

    @staticmethod
    def _get_full_path(path):
        """
        Calculates the full path to the item
        :param path: str, item path
        :return: str
        """
        path = path[1:] if path.startswith('/') else path
        return '%(root)s:/%(path)s' % dict(root=OneDriveUtil.DRIVE_ROOT,
                                           path=path)

    def _init_item_to_update(self, item_id=None, item_path=None,
                             parent_id=None, parent_path=None):
        """
        Init parent reference and item
        :param item_id:
        :param item_path:
        :param parent_id:
        :param parent_path:
        :return: tuple
        """
        ref = onedrivesdk.ItemReference()
        ref.id = parent_id
        ref.path = self._get_full_path(parent_path)

        return self.client.item(id=item_id, path=item_path), ref
