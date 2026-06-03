from uuid import UUID

from app.domain.event.aggregate import Event
from app.domain.event.repository import IEventRepository


class EventRepository(IEventRepository):
    def __init__(self):
        self._events: dict[UUID, Event] = {}

    def save(self, event: Event) -> None:
        self._events[event.id] = event

    def find_by_id(self, event_id: UUID) -> Event | None:
        return self._events.get(event_id)