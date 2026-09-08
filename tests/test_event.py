from datetime import time

from models.event import Event
from models.time_interval import TimeInterval


def test_event_overlaps():
    event = Event(
        "Alice",
        "Morning meeting",
        TimeInterval(
            time(8, 0),
            time(9, 30)
        )
    )

    other_interval = TimeInterval(
        time(9, 0),
        time(10, 0)
    )

    assert event.time_interval.overlaps(other_interval)


def test_event_does_not_overlap():
    event = Event(
        "Alice",
        "Morning meeting",
        TimeInterval(
            time(8, 0),
            time(9, 30)
        )
    )

    other_interval = TimeInterval(
        time(9, 30),
        time(10, 30)
    )

    assert not event.time_interval.overlaps(other_interval)