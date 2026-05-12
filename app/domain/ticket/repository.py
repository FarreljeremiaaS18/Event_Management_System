from abc import ABC, abstractmethod

from app.domain.ticket.entity import Ticket
from app.domain.ticket.value_objects import TicketCode


class ITicketRepository(ABC):

    @abstractmethod
    def find_by_code(self, code: TicketCode) -> Ticket | None:
        ...

    @abstractmethod
    def save(self, ticket: Ticket) -> None:
        ...