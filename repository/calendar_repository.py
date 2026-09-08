import csv
from datetime import datetime

from models.event import Event
from models.time_interval import TimeInterval
from repository.calendar_repository_interface import CalendarRepositoryInterface


class CalendarRepository(CalendarRepositoryInterface):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_events(self) -> list[Event]:
        events = []

        with open(self.file_path, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                person_name = row[0]
                subject = row[1]

                start_time = datetime.strptime(
                    row[2],
                    "%H:%M"
                ).time()

                end_time = datetime.strptime(
                    row[3],
                    "%H:%M"
                ).time()

                time_interval = TimeInterval(
                    start_time,
                    end_time
                )

                event = Event(
                    person_name,
                    subject,
                    time_interval
                )

                events.append(event)

        return events