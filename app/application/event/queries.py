from dataclasses import dataclass
from typing import List
from app.application.event.commands import EventDTO

@dataclass(frozen=True)
class GetAvailableEventsQuery:
    location_filter: str = None

class IEventQueryRepository:
    def get_published_events(self, location: str = None) -> List[EventDTO]:
        pass

class GetAvailableEventsQueryHandler:
    def __init__(self, query_repository: IEventQueryRepository):
        self.query_repository = query_repository

    def execute(self, query: GetAvailableEventsQuery) -> List[EventDTO]:
        return self.query_repository.get_published_events(query.location_filter)