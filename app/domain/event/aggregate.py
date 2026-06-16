from uuid import UUID, uuid4
from datetime import datetime
from typing import List

from app.domain.shared.aggregate_root import AggregateRoot
from app.domain.shared.errors import DomainError
from app.domain.event.value_objects import EventStatus
from app.domain.event.ticket_category import TicketCategory
from app.domain.event.events import EventCreated, EventPublished, EventCancelled

class Event(AggregateRoot):
    def __init__(
            self,
            name: str,
            description: str,
            start_date: datetime,
            end_date: datetime,
            location: str,
            max_capacity: int,
    ):
        super().__init__()

        if max_capacity <= 0:
            raise DomainError("Max capacity must be greater than zero")
        if end_date < start_date:
            raise DomainError("End date must be after start date")
        
        self.id: UUID = uuid4()
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.max_capacity = max_capacity

        self.status = EventStatus.DRAFT
        
        self._ticket_categories: List[TicketCategory] = []

        self.add_domain_event(EventCreated(event_id_ref=self.id))

    
    def add_ticket_category(self, category: TicketCategory):
        current_total_quota = sum(c.quota for c in self._ticket_categories)
        if current_total_quota + category.quota > self.max_capacity:
            raise DomainError("Total quota of ticket categories cannot exceed max capacity")
        
        if category.sales_end_date > self.start_date:
            raise DomainError("Ticket sales end date must be before event start date")
        
        self._ticket_categories.append(category)
    
    def disable_ticket_category(self, category_id: UUID):
        for category in self._ticket_categories:
            if category.id == category_id:
                category.disable()
                return
        raise DomainError("Kategori tiket tidak ditemukan di dalam event ini.")
    
    def publish(self):
        if self.status != EventStatus.DRAFT:
            raise DomainError("Only events in draft status can be published")
        
        active_categories = [c for c in self._ticket_categories if c.is_active]
        if not active_categories:
            raise DomainError("Cannot publish event without active ticket categories")
        
        self.status = EventStatus.PUBLISHED
        self.add_domain_event(EventPublished(event_id_ref=self.id))
    
    def cancel(self):
        if self.status != EventStatus.PUBLISHED:
            raise DomainError("Only published events can be canceled")
        
        self.status = EventStatus.CANCELLED
        self.add_domain_event(EventCancelled(event_id_ref=self.id))

    @property
    def ticket_categories(self) -> List[TicketCategory]:
        return self._ticket_categories.copy()