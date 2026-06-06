from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.booking.aggregate import Booking
from app.domain.ticket.value_objects import TicketCode


class IBookingRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: UUID) -> Booking | None:
        ...

    @abstractmethod
    def find_by_customer_and_event(
        self, customer_id: UUID, event_id: UUID
    ) -> Booking | None:
        ...

    @abstractmethod
    def find_pending_expired(self) -> list[Booking]:
        ...

    @abstractmethod
    def find_by_ticket_code(self, code: TicketCode) -> Booking | None:
        ...

    @abstractmethod
    def save(self, booking: Booking) -> None:
        ...