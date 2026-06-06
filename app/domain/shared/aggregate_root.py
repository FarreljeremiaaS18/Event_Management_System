from typing import List
from app.domain.shared.domain_event import DomainEvent

class AggregateRoot:
    def __init__(self):
        self._domain_events: List[DomainEvent] = []

    def add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def collect_events(self) -> List[DomainEvent]:
        events = self._domain_events.copy()
        self.clear_domain_events()
        return events

    def clear_domain_events(self):
        self._domain_events.clear()

    @property
    def domain_events(self) -> List[DomainEvent]:
        return self._domain_events.copy()