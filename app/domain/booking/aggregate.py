from uuid import UUID
from datetime import datetime, timedelta, UTC
from decimal import Decimal

from app.domain.shared.aggregate_root import AggregateRoot
from app.domain.shared.errors import DomainError
from app.domain.booking.value_objects import BookingId, BookingStatus
from app.domain.booking.events import BookingCreated, BookingPaid, BookingExpired
from app.domain.ticket.entity import Ticket


PAYMENT_DEADLINE_MINUTES = 15  # BR18


class Booking(AggregateRoot):
    def __init__(
        self,
        id: BookingId,
        customer_id: UUID,
        event_id: UUID,
        category_id: UUID,
        quantity: int,
        unit_price,          # Money
        status: BookingStatus = BookingStatus.PENDING_PAYMENT,
        payment_deadline: datetime | None = None,
        tickets: list[Ticket] | None = None,
    ):
        super().__init__()
        self.id = id
        self.customer_id = customer_id
        self.event_id = event_id
        self.category_id = category_id
        self.quantity = quantity
        self.total_price = unit_price.multiply(quantity)  # BR23
        self.status = status
        self.payment_deadline = payment_deadline
        self._tickets: list[Ticket] = tickets or []

    @classmethod
    def create(
        cls,
        customer_id: UUID,
        event_id: UUID,
        category_id: UUID,
        quantity: int,
        unit_price,          # Money
    ) -> "Booking":
        """
        Factory method — validasi quantity dan buat booking baru.
        Pemanggil (application layer) bertanggung jawab memvalidasi
        BR15 (event Published) dan BR17 (satu booking per customer per event).
        """
        if quantity <= 0:  # BR16
            raise DomainError("Quantity must be greater than zero")

        booking = cls(
            id=BookingId.generate(),
            customer_id=customer_id,
            event_id=event_id,
            category_id=category_id,
            quantity=quantity,
            unit_price=unit_price,
            payment_deadline=datetime.now(UTC) + timedelta(minutes=PAYMENT_DEADLINE_MINUTES),
        )

        booking.add_domain_event(
            BookingCreated(
                booking_id_ref=booking.id.value,
                customer_id_ref=customer_id,
                event_id_ref=event_id,
                category_id_ref=category_id,
                quantity=quantity,
            )
        )
        return booking

    def pay(self, amount) -> None:
        if self.status == BookingStatus.EXPIRED:
            raise DomainError("Cannot pay an expired booking")  # BR20
        if self.status != BookingStatus.PENDING_PAYMENT:
            raise DomainError("Booking is not in pending payment status")
        if datetime.now(UTC) > self.payment_deadline:
            raise DomainError("Payment deadline has passed")  # BR20
        if amount != self.total_price:
            raise DomainError("Payment amount does not match total price")  # BR19

        self.status = BookingStatus.PAID
        self._tickets = [Ticket.issue(self.id.value) for _ in range(self.quantity)]  # BR24

        self.add_domain_event(
            BookingPaid(
                booking_id_ref=self.id.value,
                customer_id_ref=self.customer_id,
                event_id_ref=self.event_id,
                quantity=self.quantity,
            )
        )

    def expire(self) -> None:
        if self.status == BookingStatus.PAID:
            raise DomainError("A paid booking cannot be expired") # BR21
        if self.status != BookingStatus.PENDING_PAYMENT:
            return

        self.status = BookingStatus.EXPIRED
        self.add_domain_event(
            BookingExpired(
                booking_id_ref=self.id.value,
                event_id_ref=self.event_id,
                category_id_ref=self.category_id,
                quantity=self.quantity,
            )
        )

    def mark_refunded(self) -> None:
        if self.status != BookingStatus.PAID:
            raise DomainError("Only paid bookings can be refunded")

        for ticket in self._tickets:
            ticket.cancel()

        self.status = BookingStatus.REFUNDED

    @property
    def tickets(self) -> list[Ticket]:
        return self._tickets.copy()