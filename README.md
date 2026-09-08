# Calendar Availability Project

A Python project that calculates available meeting times for a group of people based on their calendar events.

## Overview

The application reads calendar events from a CSV file and finds the starting times at which all requested people are simultaneously available for a meeting of a requested duration.

The working day is:

- **Start:** 07:00
- **End:** 19:00

For example, for Alice and Jack with a 60-minute meeting, the application returns:

```text
07:00
09:40
14:00
17:00
```

## Project Structure

```text
python-project/
├── io_comp/
│   ├── __init__.py
│   └── app.py
├── models/
│   ├── __init__.py
│   ├── event.py
│   └── time_interval.py
├── repository/
│   ├── __init__.py
│   ├── calendar_repository.py
│   └── calendar_repository_interface.py
├── services/
│   ├── __init__.py
│   └── calendar_service.py
├── resources/
│   └── calendar.csv
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_event.py
│   ├── test_calendar_repository.py
│   ├── test_calendar_service.py
│   └── test_time_interval.py
├── README.md
├── requirements.txt
└── setup.py
```

## Architecture

The project is organized into separate layers with clear responsibilities.

### Models

The `models` package contains the domain objects:

- `Event` represents a person's calendar event.
- `TimeInterval` represents a valid time range and contains time-interval behavior such as overlap detection.

`Event` uses composition by containing a `TimeInterval`.

### Repository

The repository layer is responsible for loading calendar data.

- `CalendarRepository` reads events from the CSV file and converts them into domain objects.
- `CalendarRepositoryInterface` defines the contract that a calendar data source must implement.

This keeps the service independent of the CSV format and makes it possible to replace the data source later, for example with a database or API.

### Service

`CalendarService` contains the main application logic.

It:

1. Gets events from the repository.
2. Calculates each person's available intervals during the working day.
3. Intersects the availability of all requested people.
4. Filters intervals that are long enough for the requested meeting.
5. Returns the available starting times.

### Application

`io_comp/app.py` is the entry point of the application.

It is responsible for:

- Reading user input.
- Validating and converting the input.
- Calling the service.
- Displaying the available starting times.

The application layer does not contain the calendar calculation logic.

## CSV Format

The calendar data is stored in:

```text
resources/calendar.csv
```

Each row has the following format:

```text
Person name,Event subject,Event start time,Event end time
```

Example:

```text
Alice,Morning meeting,8:00,9:30
Jack,Sales call,9:00,9:40
```

Times use the `HH:MM` format.

## Running the Application

From the project root:

```powershell
python -m io_comp.app
```

The application asks for:

1. People's names, separated by commas.
2. Meeting duration in minutes.

Example:

```text
Enter people's names separated by commas: Alice, Jack
Enter meeting duration in minutes: 60
```

## Running the Tests

Install the test dependency:

```powershell
pip install -r requirements.txt
```

Run all tests:

```powershell
python -m pytest
```

The test suite covers the main behavior of the application, including:

- Event and time-interval behavior.
- CSV repository loading.
- Meeting availability calculation.
- Edge cases such as invalid or empty input.
- Time intervals outside the working day.

## Design Goals

The project intentionally separates responsibilities so that each part has a clear purpose:

- **Models** represent domain concepts.
- **Repository** handles data access.
- **Service** contains business/application logic.
- **Application** handles user interaction.

The design also keeps the core availability logic independent from the CSV implementation, allowing the data source to be replaced in the future without changing the service logic.

## Future Extensions

The current implementation focuses on the required one-day calendar use case. The structure leaves room for future extensions such as:

- Supporting calendar dates.
- Saving newly created meetings.
- Database-backed repositories.
- API-backed repositories.
- Multiple calendar days.
- Additional scheduling constraints.

These extensions are intentionally not implemented until they are actually required.
