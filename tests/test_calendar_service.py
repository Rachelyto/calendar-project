from datetime import time, timedelta

from models.event import Event
from models.time_interval import TimeInterval
from repository.calendar_repository_interface import CalendarRepositoryInterface
from services.calendar_service import CalendarService


class FakeCalendarRepository(CalendarRepositoryInterface):

    def __init__(self, events):
        self.events = events

    def get_events(self) -> list[Event]:
        return self.events


def test_find_available_slots():
    events = [
        Event(
            "Alice",
            "Morning meeting",
            TimeInterval(time(8, 0), time(9, 30))
        ),
        Event(
            "Alice",
            "Lunch with Jack",
            TimeInterval(time(13, 0), time(14, 0))
        ),
        Event(
            "Alice",
            "Yoga",
            TimeInterval(time(16, 0), time(17, 0))
        ),
        Event(
            "Jack",
            "Morning meeting",
            TimeInterval(time(8, 0), time(8, 50))
        ),
        Event(
            "Jack",
            "Sales call",
            TimeInterval(time(9, 0), time(9, 40))
        ),
        Event(
            "Jack",
            "Lunch with Alice",
            TimeInterval(time(13, 0), time(14, 0))
        ),
        Event(
            "Jack",
            "Yoga",
            TimeInterval(time(16, 0), time(17, 0))
        ),
    ]

    repository = FakeCalendarRepository(events)
    service = CalendarService(repository)

    available_slots = service.find_available_slots(
        ["Alice", "Jack"],
        timedelta(minutes=60)
    )

    assert available_slots == [
        time(7, 0),
        time(9, 40),
        time(14, 0),
        time(17, 0)
    ]

def test_find_available_slots_returns_empty_when_duration_is_too_long():
    events = [
        Event(
            "Alice",
            "Morning meeting",
            TimeInterval(time(8, 0), time(9, 30))
        ),
    ]

    repository = FakeCalendarRepository(events)
    service = CalendarService(repository)

    available_slots = service.find_available_slots(
        ["Alice"],
        timedelta(hours=13)
    )

    assert available_slots == []

def test_find_available_slots_returns_empty_for_empty_person_list():
    repository = FakeCalendarRepository([])
    service = CalendarService(repository)

    available_slots = service.find_available_slots(
        [],
        timedelta(minutes=60)
    )

    assert available_slots == []

def test_find_available_slots_returns_empty_for_zero_duration():
    repository = FakeCalendarRepository([])
    service = CalendarService(repository)

    available_slots = service.find_available_slots(
        ["Alice"],
        timedelta(minutes=0)
    )

    assert available_slots == []

def test_find_available_slots_returns_empty_for_negative_duration():
    repository = FakeCalendarRepository([])
    service = CalendarService(repository)

    available_slots = service.find_available_slots(
        ["Alice"],
        timedelta(minutes=-30)
    )

    assert available_slots == []

def test_find_available_slots_returns_full_day_for_person_without_events():
    repository = FakeCalendarRepository([])
    service = CalendarService(repository)

    available_slots = service.find_available_slots(
        ["Alice"],
        timedelta(hours=1)
    )

    assert available_slots == [
        time(7, 0)
    ]

def test_find_available_slots_ignores_events_outside_working_hours():
    events = [
        Event(
            "Alice",
            "Early meeting",
            TimeInterval(time(5, 0), time(6, 0))
        ),
        Event(
            "Alice",
            "Late meeting",
            TimeInterval(time(20, 0), time(21, 0))
        ),
    ]

    repository = FakeCalendarRepository(events)
    service = CalendarService(repository)

    available_slots = service.find_available_slots(
        ["Alice"],
        timedelta(hours=1)
    )

    assert available_slots == [
        time(7, 0)
    ]