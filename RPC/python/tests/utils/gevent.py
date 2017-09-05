"""Test helpers and utilities related to Gevent."""
import time

import gevent


def wait_until(condition, objects=None, timeout=None, count=None):
    """Helper that waits until 'condition' is fulfilled.

    Besides 'condition' takes the same arguments as ``gevent.wait()``.
    """
    timestamp = time.time()
    while True:
        gevent.wait(
            objects=objects,
            count=count,
            timeout=0.01
        )
        if condition():
            return True

        if (timeout is not None and
            (time.time() - timestamp) > timeout):
            return False
