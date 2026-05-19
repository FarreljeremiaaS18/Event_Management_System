from app.application.event.commands import CreateEventCommand, EventDTO
from app.domain.event.aggregate import Event
from app.domain.event.repository import IEventRepository

class CreateEventCommandHandler:
    def __init__(self, event_repository: IEventRepository):
        self.repository = event_repository
    
    def execute(self, command: CreateEventCommand) -> EventDTO:
        event = Event(
            name=command.name,
            description=command.description,
            start_date=command.start_date,
            end_date=command.end_date,
            location=command.location,
            max_capacity=command.max_capacity
        )
        self.repository.save(event)
        return EventDTO(
            event_id=event.id,
            name=event.name,
            status=event.status.value
        )