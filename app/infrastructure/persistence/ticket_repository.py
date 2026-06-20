from uuid import UUID
from app.domain.ticket.entity import Ticket
from app.domain.ticket.repository import ITicketRepository
from app.domain.ticket.value_objects import TicketCode, TicketStatus, TicketId
from app.infrastructure.persistence.db import SessionLocal
from app.infrastructure.persistence.models import TicketModel


class TicketRepository(ITicketRepository):
    def find_by_code(self, code: TicketCode) -> Ticket | None:
        with SessionLocal() as session:
            model = session.query(TicketModel).filter(TicketModel.code == code.value).first()
            if model:
                return Ticket(
                    id=TicketId(UUID(model.id)),
                    booking_id=UUID(model.booking_id),
                    code=TicketCode(model.code),
                    status=TicketStatus(model.status),
                    checked_in_at=model.checked_in_at
                )
            return None
        
    def save(self, ticket: Ticket) -> None:
        with SessionLocal() as session:
            model = session.query(TicketModel).filter(TicketModel.id == str(ticket.id.value)).first()
            if model:
                model.status = ticket.status.value
                model.checked_in_at = ticket.checked_in_at
                session.commit()