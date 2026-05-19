from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class CreateEventCommand:
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    max_capacity: int

@dataclass(frozen=True)
class EventDTO:
    event_id: UUID
    name: str
    status: str