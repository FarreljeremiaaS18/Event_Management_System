from dataclasses import dataclass
from typing import List, Any
from uuid import UUID
from app.application.event.commands import EventDTO

@dataclass(frozen=True)
class GetAvailableEventsQuery:
    location_filter: str = None

@dataclass(frozen=True)
class GetEventDetailsQuery:
    event_id: UUID

@dataclass(frozen=True)
class GetEventSalesReportQuery:
    event_id: UUID

@dataclass(frozen=True)
class GetEventParticipantsQuery:
    event_id: UUID

class IEventQueryRepository:
    def get_published_events(self, location: str = None) -> List[EventDTO]:
        pass

    def get_event_details(self, event_id: UUID) -> Any: 
        pass

    def get_sales_report(self, event_id: UUID) -> Any:
        pass

    def get_participants(self, event_id: UUID) -> List[Any]:
        pass


class GetAvailableEventsQueryHandler:
    def __init__(self, query_repository: IEventQueryRepository):
        self.query_repository = query_repository

    def execute(self, query: GetAvailableEventsQuery) -> List[EventDTO]:
        return self.query_repository.get_published_events(query.location_filter)

class GetEventDetailsQueryHandler:
    def __init__(self, query_repository: IEventQueryRepository):
        self.query_repository = query_repository

    def execute(self, query: GetEventDetailsQuery) -> Any:
        return self.query_repository.get_event_details(query.event_id)

class GetEventSalesReportQueryHandler:
    def __init__(self, query_repository: IEventQueryRepository):
        self.query_repository = query_repository

    def execute(self, query: GetEventSalesReportQuery) -> Any:
        return self.query_repository.get_sales_report(query.event_id)

class GetEventParticipantsQueryHandler:
    def __init__(self, query_repository: IEventQueryRepository):
        self.query_repository = query_repository

    def execute(self, query: GetEventParticipantsQuery) -> List[Any]:
        return self.query_repository.get_participants(query.event_id)

