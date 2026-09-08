from datetime import datetime, time, timedelta

from models.event import Event
from models.time_interval import TimeInterval
from repository.calendar_repository_interface import CalendarRepositoryInterface


class CalendarService:
    DAY_START = time(7, 0)
    DAY_END = time(19, 0)

    def __init__(self, repository: CalendarRepositoryInterface):
        self.repository = repository

    def find_available_slots(
            self,
            person_list: list[str],
            event_duration: timedelta
    ) -> list[time]:

        if not person_list:
            return []

        if event_duration <= timedelta(0):
            return []

        events = self.repository.get_events()

        available_intervals = [
            TimeInterval(
                self.DAY_START,
                self.DAY_END
            )
        ]

        for person in person_list:
            person_events = [
                event
                for event in events
                if event.person_name == person
            ]

            person_events.sort(
                key=lambda event: event.time_interval.start_time
            )

            person_available = self._find_available_intervals(
                person_events
            )

            available_intervals = self._intersect_intervals(
                available_intervals,
                person_available
            )

        return [
            interval.start_time
            for interval in available_intervals
            if self._duration_between(
                interval.start_time,
                interval.end_time
            ) >= event_duration
        ]


    def _find_available_intervals(
            self,
            events: list[Event]
    ) -> list[TimeInterval]:
        available_intervals = []

        current_time = self.DAY_START

        for event in events:
            event_start = event.time_interval.start_time
            event_end = event.time_interval.end_time

            if event_end <= self.DAY_START:
                continue

            if event_start >= self.DAY_END:
                break

            event_start = max(
                event_start,
                self.DAY_START
            )

            event_end = min(
                event_end,
                self.DAY_END
            )

            if current_time < event_start:
                available_intervals.append(
                    TimeInterval(
                        current_time,
                        event_start
                    )
                )

            if event_end > current_time:
                current_time = event_end

        if current_time < self.DAY_END:
            available_intervals.append(
                TimeInterval(
                    current_time,
                    self.DAY_END
                )
            )

        return available_intervals

    def _intersect_intervals(
            self,
            first_intervals: list[TimeInterval],
            second_intervals: list[TimeInterval]
    ) -> list[TimeInterval]:

        intersections = []

        first_index = 0
        second_index = 0

        while (
                first_index < len(first_intervals)
                and second_index < len(second_intervals)
        ):
            first_interval = first_intervals[first_index]
            second_interval = second_intervals[second_index]

            start = max(
                first_interval.start_time,
                second_interval.start_time
            )

            end = min(
                first_interval.end_time,
                second_interval.end_time
            )

            if start < end:
                intersections.append(
                    TimeInterval(start, end)
                )

            if first_interval.end_time < second_interval.end_time:
                first_index += 1
            else:
                second_index += 1

        return intersections

    @staticmethod
    def _duration_between(
            start_time: time,
            end_time: time
    ) -> timedelta:

        start = datetime.combine(
            datetime.today(),
            start_time
        )

        end = datetime.combine(
            datetime.today(),
            end_time
        )

        return end - start