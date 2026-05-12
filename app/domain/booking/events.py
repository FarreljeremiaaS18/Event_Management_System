from uuid import UUID
from pydantic import Field
from app.domain.shared.domain_event import DomainEvent


class BookingCreated(DomainEvent):
    booking_id_ref: UUID
    customer_id_ref: UUID
    event_id_ref: UUID
    category_id_ref: UUID
    quantity: int


class BookingPaid(DomainEvent):
    booking_id_ref: UUID
    customer_id_ref: UUID
    event_id_ref: UUID
    quantity: int


class BookingExpired(DomainEvent):
    booking_id_ref: UUID
    event_id_ref: UUID
    category_id_ref: UUID
    quantity: int