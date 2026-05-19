from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.event.aggregate import Event

class IEventRepository(ABC):
    
    @abstractmethod
    def save(self, event: Event) -> None:
        ...

    @abstractmethod
    def find_by_id(self, event_id: UUID) -> Event | None:
        ...