from app.infrastructure.persistence.event_repository import EventRepository
from app.application.event.handlers import CreateEventCommandHandler


event_repository = EventRepository()

def get_create_event_handler() -> CreateEventCommandHandler:
  
    return CreateEventCommandHandler(event_repository=event_repository)