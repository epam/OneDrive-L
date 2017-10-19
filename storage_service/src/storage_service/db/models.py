""" Models definition """
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

import datetime

from peewee import (
    BlobField, BooleanField, CharField, ForeignKeyField, IntegerField,
    Model, PrimaryKeyField, Proxy, TextField, TimestampField
)

database_proxy = Proxy()  # Create a proxy for our db.


class BaseModel(Model):
    """ Base model """

    class Meta:
        """ Init database as a proxy """
        database = database_proxy


class Owner(BaseModel):
    """ Owner table """
    id = PrimaryKeyField()
    user_name = CharField(max_length=50)
    user_id = CharField(max_length=100)
    user_email = CharField(max_length=50, unique=True)


class Item(BaseModel):
    """ Item table """
    id = PrimaryKeyField()
    user_id = ForeignKeyField(Owner)
    path = TextField()
    e_tag = TextField()
    c_tag = TextField()
    sha1_hash = BlobField()
    crc32_hash = BlobField()
    quick_xor_hash = BlobField()
    is_dir = BooleanField()
    is_deleted = BooleanField()
    last_modified_date_time = TimestampField()
    size = IntegerField()
    local = BooleanField(default=False)


class Setting(BaseModel):
    """ Setting table """
    id = PrimaryKeyField()
    user_id = ForeignKeyField(Owner)
    name = CharField(max_length=50)
    value = TextField()
    date_time = TimestampField(default=datetime.datetime.now)
