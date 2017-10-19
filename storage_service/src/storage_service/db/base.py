""" Provides useful functionality to init engine """
# pylint: disable=import-error

import os

from db import models
from onedrive_client.utils import ONEDRIVE_CONFIG_DIR
from onedrive_client.utils.config import config_load
from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase

_ONEDRIVE_STORAGE_CFG = 'db.conf'
_ONEDRIVE_STORAGE_CFG_PATH = os.path.join(ONEDRIVE_CONFIG_DIR,
                                          _ONEDRIVE_STORAGE_CFG)

_ONEDRIVE_STORAGE_CFG_MANDATORY_KEYS = ('db_name',)
_ONEDRIVE_STORAGE_TYPES = {
    'sqlite': SqliteDatabase,
    'mysql': MySQLDatabase,
    'postgresql': PostgresqlDatabase,
}


def _validate_db_conf(conf):
    """ Validates DB config """
    keys = conf.keys()

    for key in _ONEDRIVE_STORAGE_CFG_MANDATORY_KEYS:
        if key not in keys:
            raise KeyError('The {key} key is mandatory'.format(key=key))

    # add default keys
    if not conf.get('connect_attr'):
        conf['connect_attr'] = {}


def _load_db_config(name):
    """
    Gets DB attribs by name
    :param name:
    :return: dict
    """

    if not os.path.exists(_ONEDRIVE_STORAGE_CFG_PATH):
        mess = '{file} doe not exist'.format(file=_ONEDRIVE_STORAGE_CFG_PATH)
        raise FileNotFoundError(mess)

    db_attr = config_load(_ONEDRIVE_STORAGE_CFG_PATH)

    conf = db_attr.get(name)
    if conf is None:
        mess = 'Unable to load configuration {name} from ' \
               '{file}'.format(name=name, file=_ONEDRIVE_STORAGE_CFG_PATH)
        raise KeyError(mess)

    _validate_db_conf(conf)

    return conf


def create_engine(name):
    """
    Initialises proper DB engine
    :param name: str, the name of engine
    :return: Database instance
    """
    conf = _load_db_config(name)

    if name not in _ONEDRIVE_STORAGE_TYPES:
        mess = 'Database type {db} is not supported'.format(db=name)
        raise NotImplementedError(mess)

    db_inst = _ONEDRIVE_STORAGE_TYPES.get(name)
    db_name = conf['db_name']

    if isinstance(db_inst, SqliteDatabase):
        db_name = os.path.join(ONEDRIVE_CONFIG_DIR, conf['db_name'])

    database = db_inst(db_name, **conf['connect_attr'])

    # Configure our proxy to use the db we specified in config.
    models.database_proxy.initialize(database)

    return database


def create_tables(database):
    """
    Creates tables if they don't exist
    :param database:
    """
    tables = [models.Owner, models.Item, models.Setting]
    database.create_tables(tables, safe=True)
