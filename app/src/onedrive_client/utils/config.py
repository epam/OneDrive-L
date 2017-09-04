"""
Provides functionality for working with configuration files in YAML format
"""

import os

from onedrive_client.utils.errors import OneDriveConfigException
import yaml


def config_load(file_path):
    """
    :param file_path: full path to configuration file
    :return: content of the configuration file as dictionary
    """

    if not os.path.isfile(file_path):
        raise OneDriveConfigException('{} is missing'.format(file_path))

    with open(file_path, 'r') as stream:
        try:
            content = yaml.load(stream)
        except Exception as exc:
            message = 'Failed to load configuration file:\n{}'.format(exc)
            raise OneDriveConfigException(message)

    return content
