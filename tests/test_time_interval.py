from datetime import time

from models.time_interval import TimeInterval


def test_time_interval_overlaps():
    interval = TimeInterval(
        time(8, 0),
        time(9, 30)
    )

    other_interval = TimeInterval(
        time(9, 0),
        time(10, 0)
    )

    assert interval.overlaps(other_interval)

import pytest

from datetime import time

from models.time_interval import TimeInterval


def test_time_interval_rejects_invalid_interval():
    with pytest.raises(ValueError):
        TimeInterval(
            time(10, 0),
            time(9, 0)
        )