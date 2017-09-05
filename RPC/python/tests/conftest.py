"""Tests configuration and common fixtures."""
import logbook
import pytest


@pytest.fixture
def timeout():
    """Common timeout."""
    return 5


@pytest.fixture
def local_address():
    """Local address used for tests."""
    return ('127.0.0.1', 6558)


def pytest_configure():
    """Session-wise configuration."""
    # Logging configuration.
    handler = logbook.StderrHandler(
        level=logbook.TRACE,
        format_string=(
            '[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] '
            '{record.level_name}: '
            '{record.channel} ({record.func_name}:{record.lineno}): '
            '{record.message}'
        )
    )
    handler.push_application()
