"""Logbook-related utils."""
from logbook import Logger as LogbookLogger


class Logger(LogbookLogger):
    """Provides additional capabilities over standard ``Logger``.

    - Makes possible to pass 'processor' which alters log-records.
    """
    def __init__(self, *args, processor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__processor = processor

    def process_record(self, record):
        super().process_record(record)
        if self.__processor is not None:
            self.__processor(record)
