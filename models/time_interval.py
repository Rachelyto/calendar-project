from datetime import time


class TimeInterval:

    def __init__(self, start_time: time, end_time: time):
        if start_time >= end_time:
            raise ValueError("Start time must be before end time.")

        self.start_time = start_time
        self.end_time = end_time

    def overlaps(self, other: "TimeInterval") -> bool:
        return (
            self.start_time < other.end_time
            and other.start_time < self.end_time
        )