from app.application.event.commands import (
    CreateEventCommand, 
    PublishEventCommand, 
    CancelEventCommand, 
    CreateTicketCategoryCommand, 
    DisableTicketCategoryCommand, 
    EventDTO
)
from app.domain.event.aggregate import Event
from app.domain.event.ticket_category import TicketCategory
from app.domain.event.repository import IEventRepository
from app.domain.shared.value_objects import Money 

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

class PublishEventCommandHandler:
    def __init__(self, repository: IEventRepository):
        self.repository = repository

    def execute(self, command: PublishEventCommand) -> EventDTO:
        event = self.repository.find_by_id(command.event_id)
        event.publish() 
        self.repository.save(event)
        return EventDTO(event_id=event.id, name=event.name, status=event.status.value)

class CancelEventCommandHandler:
    def __init__(self, repository: IEventRepository):
        self.repository = repository

    def execute(self, command: CancelEventCommand) -> EventDTO:
        event = self.repository.find_by_id(command.event_id)
        event.cancel()
        self.repository.save(event)
        return EventDTO(event_id=event.id, name=event.name, status=event.status.value)

class CreateTicketCategoryCommandHandler:
    def __init__(self, repository: IEventRepository):
        self.repository = repository

    
    def execute(self, command: CreateTicketCategoryCommand) -> EventDTO:
        event = self.repository.find_by_id(command.event_id)
        
        harga_tiket = Money(command.price)
        kategori_baru = TicketCategory(
            name=command.name,
            price=harga_tiket,
            quota=command.quota,
            sales_start_date=command.sales_start_date,
            sales_end_date=command.sales_end_date
        )
        
        event.add_ticket_category(kategori_baru)
        
        self.repository.save(event)
        return EventDTO(event_id=event.id, name=event.name, status=event.status.value)

class DisableTicketCategoryCommandHandler:
    def __init__(self, repository: IEventRepository):
        self.repository = repository

    def execute(self, command: DisableTicketCategoryCommand) -> EventDTO:
        event = self.repository.find_by_id(command.event_id)
        
        event.disable_ticket_category(command.category_id)
        
        self.repository.save(event)
        return EventDTO(event_id=event.id, name=event.name, status=event.status.value)