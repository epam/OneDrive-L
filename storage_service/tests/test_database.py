"""
Tests for the DataBase class interfaces
"""

import os

import pytest

from storage_service.database import DataBase


# pylint: disable=invalid-name
# pylint: disable=expression-not-assigned
DataBase.file_path = os.path.dirname(os.path.abspath(__file__))
ITEM = dict(id='01R7X2ASPKO3KLGA22BNE36WQTAYXEJE2D'.encode(),
            name='kt_rev1.docx',
            path='/drive/root:',
            e_tag='\"{B3D476EA-5A03-490B-BF5A-13062E449343},56\"'.encode(),
            c_tag='\"c:{B3D476EA-5A03-490B-BF5A-13062E449343},19\"'.encode(),
            quick_xor_hash='m0jiJsjCKPQFbKYadzKeYp1NIC8='.encode(),
            is_dir=False,
            is_deleted=False,
            last_modified_date_time=20170104134558)


def teardown_function():
    """
    Removes database after each test execution
    """
    try:
        os.remove(os.path.join(DataBase.file_path, 'onedrive.sqlite'))
    except FileNotFoundError:
        pass


def test_db_connection():
    """
    Test database connection
    """

    db = DataBase()
    db.connect()
    assert db.conn, 'Connection with database was not established'
    assert db.cursor, 'Cursor object was not set'

    db.disconnect()


def test_db_connection_context():
    """
    Test connection to database via context manager
    """

    with DataBase() as db:
        assert db.conn, 'Connection with database was not established'
        assert db.cursor, 'Cursor object was not set'


def test_db_create_table():
    """
    Test database table creation
    """

    with DataBase() as db:
        db.create_table()
        columns = db.get_columns()
        assert isinstance(columns, list)
        assert all(key in columns for key in DataBase.cols)


def test_db_insert_item():
    """
    Test databasa entity insert
    """

    with DataBase() as db:
        db.create_table()
        db.insert_item(ITEM)
        db_items = db.get_item('name', ITEM['name'])
        assert all(db_items[0].get(key, 'no') == ITEM[key] for key in ITEM),\
            'Missing keys in database entry'


def test_db_get_item():
    """
    Test database get_item functionality
    """

    with DataBase() as db:
        db.create_table()
        db.insert_item(ITEM)
        db_items = db.get_item('name', ITEM['name'])
        assert isinstance(db_items, list)
        assert isinstance(db_items[0], dict)
        assert not db.get_item('nocolumn', 'novalue')


def test_db_update_item():
    """
    est database entity update
    """

    item_to_upd = ITEM.copy()
    item_to_upd['size'] = 123456

    with DataBase() as db:
        db.create_table()
        db.insert_item(ITEM)
        db.update_item(item_to_upd, 1)
        db_item = db.get_item('rowid', 1)[0]
        assert db_item.get('size', None) == 123456,\
            'Database entry was not updated'


def test_db_delete_item():
    """
    Test database entity removal
    """

    with DataBase() as db:
        db.create_table()
        db.insert_item(ITEM)
        db.delete_item(1)
        with pytest.raises(IndexError,
                           message='Database entry was not deleted'):
            db.get_item('rowid', 1)[0]
