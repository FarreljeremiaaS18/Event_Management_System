from uuid import UUID
from app.domain.shared.domain_event import DomainEvent

class EventCreated(DomainEvent):
    event_id_ref: UUID

class EventPublished(DomainEvent):
    event_id_ref: UUID

class EventCanceled(DomainEvent):
    event_id_ref: UUID

