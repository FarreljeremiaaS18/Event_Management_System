from uuid import UUID
from datetime import datetime
from app.domain.shared.domain_event import DomainEvent


class TicketIssued(DomainEvent):
    ticket_id_ref: UUID
    booking_id_ref: UUID
    ticket_code: str


class TicketCheckedIn(DomainEvent):
    ticket_id_ref: UUID
    booking_id_ref: UUID
    checked_in_at: datetime


class TicketCancelled(DomainEvent):
    ticket_id_ref: UUID
    booking_id_ref: UUID