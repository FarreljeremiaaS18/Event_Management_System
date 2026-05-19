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

@dataclass(frozen=True)
class PublishEventCommand:
    event_id: UUID

@dataclass(frozen=True)
class CancelEventCommand:
    event_id: UUID

@dataclass(frozen=True)
class CreateTicketCategoryCommand:
    event_id: UUID
    name: str
    price: float
    quota: int
    sales_start_date: datetime
    sales_end_date: datetime

@dataclass(frozen=True)
class DisableTicketCategoryCommand:
    event_id: UUID
    category_id: UUID