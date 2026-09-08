from datetime import timedelta

from repository.calendar_repository import CalendarRepository
from services.calendar_service import CalendarService


def main():
    repository = CalendarRepository(
        "resources/calendar.csv"
    )

    service = CalendarService(repository)

    people_input = input(
        "Enter people's names separated by commas: "
    )

    person_list = [
        person.strip()
        for person in people_input.split(",")
        if person.strip()
    ]

    duration_input = input(
        "Enter meeting duration in minutes: "
    )

    try:
        duration_minutes = int(duration_input)
    except ValueError:
        print("Meeting duration must be a number.")
        return

    if duration_minutes <= 0:
        print("Meeting duration must be greater than 0.")
        return

    event_duration = timedelta(minutes=duration_minutes)

    available_slots = service.find_available_slots(
        person_list,
        event_duration
    )

    if not available_slots:
        print("No available slots found.")
        return

    print("Available starting times:")

    for slot in available_slots:
        print(slot.strftime("%H:%M"))


if __name__ == "__main__":
    main()