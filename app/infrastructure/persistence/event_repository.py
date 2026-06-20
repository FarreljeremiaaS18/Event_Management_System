from uuid import UUID

from app.domain.event.aggregate import Event
from app.domain.event.repository import IEventRepository
from app.infrastructure.persistence.db import SessionLocal
from app.infrastructure.persistence.models import EventModel
from app.infrastructure.persistence.mappers import EventMapper


class EventRepository(IEventRepository):
    def save(self, event: Event) -> None:
        with SessionLocal() as session:
            model = EventMapper.to_model(event)
            session.merge(model)
            session.commit()

    def find_by_id(self, event_id: UUID) -> Event | None:
        with SessionLocal() as session:
            model = session.query(EventModel).filter(EventModel.id == str(event_id)).first()
            if model:
                return EventMapper.to_domain(model)
            return None