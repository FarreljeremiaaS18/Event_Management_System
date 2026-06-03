from app.domain.ticket.entity import Ticket
from app.domain.ticket.repository import ITicketRepository
from app.domain.ticket.value_objects import TicketCode


class TicketRepository(ITicketRepository):
    def __init__(self):
        self._tickets: dict[str, Ticket] = {}

    def find_by_code(self, code: TicketCode) -> Ticket | None:
        return self._tickets.get(code.value)

    def save(self, ticket: Ticket) -> None:
        self._tickets[ticket.code.value] = ticket