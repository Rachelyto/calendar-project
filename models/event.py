from models.time_interval import TimeInterval


class Event:

    def __init__(
        self,
        person_name: str,
        subject: str,
        time_interval: TimeInterval
    ):
        self.person_name = person_name
        self.subject = subject
        self.time_interval = time_interval

    def __str__(self) -> str:
        return (
            f"{self.person_name}: "
            f"{self.subject} "
            f"({self.time_interval.start_time.strftime('%H:%M')} - "
            f"{self.time_interval.end_time.strftime('%H:%M')})"
        )