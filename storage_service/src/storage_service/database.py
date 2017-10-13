"""
Provides interfaces for communication with SQLite database
"""

import os
from pathlib import Path
import sqlite3

from .exceptions import StorageServiceException


def dict_factory(cursor, row):
    """
    :param cursor: cursor object
    :param row: row
    :return: dictionary with select results
    """

    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary


class DataBase(object):
    """
    Class with interfaces for managing SQL queries to database
    """

    file_path = os.path.join(str(Path.home()), '.onedrive')
    cols = dict(id='BLOB',
                name='TEXT',
                path='TEXT',
                e_tag='BLOB',
                c_tag='BLOB',
                sha1_hash='BLOB',
                crc32_hash='BLOB',
                quick_xor_hash='BLOB',
                is_dir='BOOL',
                is_deleted='BOOL',
                last_modified_date_time='INT',
                size='INT')

    def __init__(self, dbname='onedrive.sqlite', table='onedrive_items'):
        self.conn = None
        self.cursor = None
        self.dbname = dbname
        self.dbpath = os.path.join(DataBase.file_path, self.dbname)
        self.table = table

        if not os.path.exists(DataBase.file_path):
            os.mkdir(DataBase.file_path, 700)

        if self.dbname:
            self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    @staticmethod
    def __declare_types():
        """
        Declares unsupported boolean type
        """

        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter('BOOL', lambda v: bool(int(v)))

    @staticmethod
    def __to_str(value: str) -> str:
        """
        :param value: string value
        :return appropriate string value for SQL query
        """

        return '\'{}\''.format(value)

    @staticmethod
    def __gen_sql_input(item: dict) -> tuple:
        """
        :param item: dictionary representation of onedrive item
        :return: tuple(tuple(comma separated columns),
        tuple(comma separated values))
        """

        col, val = [], []
        for key, value in item.items():
            col.append(key)
            val.append(value)
        return tuple(col), tuple(val)

    def connect(self):
        """
        Establishes database connection: set self.conn, self.cursor
        """

        try:
            self.conn = sqlite3.connect(self.dbpath,
                                        detect_types=sqlite3.PARSE_DECLTYPES)
            self.conn.row_factory = dict_factory
            self.__declare_types()
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            raise StorageServiceException

    def disconnect(self):
        """
        Close database connection
        """

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __write(self, query, *fvalues):
        """
        :param query: SQL query
        :param fvalues: values for the query if it is necessary
        Executes SQL queries which require commit() method
        """

        try:
            with self.conn:
                self.cursor.execute(query, *fvalues)
        except sqlite3.IntegrityError:
            raise StorageServiceException

    def get_columns(self) -> list:
        """
        :return: list of column names for the table
        """

        query = 'PRAGMA table_info({})'.format(self.table)
        self.cursor.execute(query)
        return [col['name'] for col in self.cursor.fetchall()]

    def get_item(self, column, value) -> list:
        """
        :param column: column name
        :param value: column value
        Results of the SELECT SQL query
        """

        if isinstance(value, str):
            value = self.__to_str(value)
        query = 'SELECT rowid, * FROM {} WHERE {} = {}'\
            .format(self.table, column, value)
        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError:
            return []
        return self.cursor.fetchall()

    def create_table(self):
        """
        Creates table in database if it does not exist
        """

        columns = ','.join(('{} {}'.format(k, v)
                            for k, v in DataBase.cols.items()))
        query = 'CREATE TABLE IF NOT EXISTS {} ({})'\
            .format(self.table, columns)
        self.__write(query)

    def insert_item(self, item: dict):
        """
        :param item: dictionary representation of onedrive item
        Inserts new row into database
        """

        columns, values = self.__gen_sql_input(item)
        query = 'INSERT INTO {} ({}) VALUES ({})'\
            .format(self.table, ','.join(columns),
                    ','.join(['?']*len(columns)))
        self.__write(query, values)

    def update_item(self, item: dict, rowid: int):
        """
        :param item: dictionary representation of onedrive item
        :param rowid: row number to be updated
        Updates specified row with item attributes
        """

        columns, values = self.__gen_sql_input(item)
        dataset = [column + '=?' for column in columns]
        query = 'UPDATE {} SET {} WHERE rowid = {}'\
            .format(self.table, ', '.join(dataset), rowid)
        self.__write(query, values)

    def delete_item(self, rowid: int):
        """
        :param rowid: row number to be removed
        Removes database row with specified row id
        """

        query = 'DELETE FROM {} WHERE rowid = {}'\
            .format(self.table, rowid)
        self.__write(query)
