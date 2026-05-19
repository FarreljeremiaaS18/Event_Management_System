from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class CheckInTicketCommand:
    ticket_code: str
    event_id: UUID

@dataclass(frozen=True)
class TicketDTO:
    ticket_code: str
    status: str