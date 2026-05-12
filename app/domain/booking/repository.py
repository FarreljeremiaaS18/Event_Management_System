from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.booking.aggregate import Booking


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
    def save(self, booking: Booking) -> None:
        ...