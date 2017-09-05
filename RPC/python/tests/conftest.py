"""Tests configuration and common fixtures."""
import logbook


def pytest_configure():
    # Logging configuration.
    handler = logbook.StderrHandler(
        level=logbook.TRACE,
        format_string= (
            '[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] '
            '{record.level_name}: '
            '{record.channel} ({record.func_name}:{record.lineno}): '
            '{record.message}'
        )
    )
    handler.push_application()
