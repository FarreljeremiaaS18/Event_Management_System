from uuid import UUID
from datetime import datetime, UTC

from app.domain.shared.errors import DomainError
from app.domain.ticket.value_objects import TicketId, TicketCode, TicketStatus
from app.domain.ticket.events import TicketCheckedIn, TicketCancelled


class Ticket:
    def __init__(
        self,
        id: TicketId,
        booking_id: UUID,
        code: TicketCode,
        status: TicketStatus = TicketStatus.ACTIVE,
        checked_in_at: datetime | None = None,
    ):
        self.id = id
        self.booking_id = booking_id
        self.code = code
        self.status = status
        self.checked_in_at = checked_in_at
        self._events = []

    @classmethod
    def issue(cls, booking_id: UUID) -> "Ticket":
        ticket = cls(
            id=TicketId.generate(),
            booking_id=booking_id,
            code=TicketCode.generate(),
        )
        return ticket

    def check_in(self) -> None:
        if self.status == TicketStatus.CHECKED_IN:
            raise DomainError("Ticket has already been checked in")
        if self.status == TicketStatus.CANCELLED:
            raise DomainError("Cannot check in a cancelled ticket")

        self.status = TicketStatus.CHECKED_IN
        self.checked_in_at = datetime.now(UTC)
        self._events.append(
            TicketCheckedIn(
                ticket_id_ref=self.id.value,
                booking_id_ref=self.booking_id,
                checked_in_at=self.checked_in_at,
            )
        )

    def cancel(self) -> None:
        if self.status == TicketStatus.CHECKED_IN:
            raise DomainError("Cannot cancel a ticket that has already been checked in")
        if self.status == TicketStatus.CANCELLED:
            return 
        self.status = TicketStatus.CANCELLED
        self._events.append(
            TicketCancelled(
                ticket_id_ref=self.id.value,
                booking_id_ref=self.booking_id,
            )
        )

    def collect_events(self) -> list:
        events = self._events.copy()
        self._events.clear()
        return events