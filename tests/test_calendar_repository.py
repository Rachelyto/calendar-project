from datetime import time

from repository.calendar_repository import CalendarRepository


def test_get_events():
    repository = CalendarRepository(
        "resources/calendar.csv"
    )

    events = repository.get_events()

    assert len(events) == 12

    first_event = events[0]

    assert first_event.person_name == "Alice"
    assert first_event.subject == "Morning meeting"
    assert first_event.time_interval.start_time == time(8, 0)
    assert first_event.time_interval.end_time == time(9, 30)