from abc import ABC, abstractmethod

from models.event import Event


class CalendarRepositoryInterface(ABC):

    @abstractmethod
    def get_events(self) -> list[Event]:
        pass