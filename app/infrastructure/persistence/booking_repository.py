from uuid import UUID

from app.domain.booking.aggregate import Booking
from app.domain.booking.repository import IBookingRepository
from app.domain.booking.value_objects import BookingStatus


class BookingRepository(IBookingRepository):
    def __init__(self):
        self._bookings: dict[UUID, Booking] = {}

    def find_by_id(self, id: UUID) -> Booking | None:
        return self._bookings.get(id)

    def find_by_customer_and_event(
        self,
        customer_id: UUID,
        event_id: UUID
    ) -> Booking | None:

        for booking in self._bookings.values():
            if (
                booking.customer_id == customer_id
                and booking.event_id == event_id
            ):
                return booking

        return None

    def find_pending_expired(self) -> list[Booking]:
        return [
            booking
            for booking in self._bookings.values()
            if booking.status == BookingStatus.PENDING_PAYMENT
        ]

    def save(self, booking: Booking) -> None:
        self._bookings[booking.id.value] = booking