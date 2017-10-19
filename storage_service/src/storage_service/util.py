""" Common Storage interface """
from storage_service.db.base import create_engine, create_tables


class StorageUtil(object):
    """ Provides common interface to interact with DB
    Can be used directly to initialize DB,
    on the other hand provides a context manager interface
    """

    def __init__(self, engine_name):
        self.engine = engine_name
        self.database = None

    def init_engine(self):
        """ Initialise a particular engine """
        self.database = create_engine(self.engine)
        create_tables(self.database)

    def disable_engine(self):
        """ Disable engine """
        self.database.close()

    def __enter__(self):
        """ Init storage util """
        self.init_engine()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the context related to storage util """
        self.disable_engine()

    def get_dirty_local_items(self):
        """ Retrieves dirty local items """
        pass

    def put_dirty_local_items(self):
        """ Puts dirty local items """
        pass

    def delete_dirty_local_items(self):
        """ Deletes dirty local items """
        pass

    def get_dirty_remote_items(self):
        """ Retrieves dirty remote items """
        pass

    def put_dirty_remote_items(self):
        """ Puts dirty remote items """
        pass

    def delete_dirty_remote_items(self):
        """ Deletes dirty remote items """
        pass

    def get_pristine_items(self):
        """ Retrieves pristine items """
        pass

    def put_pristine_items(self):
        """ Puts pristine items """
        pass

    def delete_pristine_items(self):
        """ Deletes pristine items """
        pass

    def get(self):
        """ Gets items """
        pass

    def put(self):
        """ Puts items """
        pass

    def delete(self):
        """ Deletes items """
        pass
