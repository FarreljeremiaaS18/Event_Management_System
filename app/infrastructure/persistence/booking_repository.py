from uuid import UUID

from app.domain.booking.aggregate import Booking
from app.domain.booking.repository import IBookingRepository
from app.domain.booking.value_objects import BookingStatus
from app.domain.ticket.value_objects import TicketCode
from app.infrastructure.persistence.db import SessionLocal
from app.infrastructure.persistence.models import BookingModel, TicketModel
from app.infrastructure.persistence.mappers import BookingMapper


class BookingRepository(IBookingRepository):
    def find_by_id(self, id: UUID) -> Booking | None:
        with SessionLocal() as session:
            model = session.query(BookingModel).filter(BookingModel.id == str(id)).first()
            if model:
                return BookingMapper.to_domain(model)
            return None

    def find_by_customer_and_event(self, customer_id: UUID, event_id: UUID) -> Booking | None:
        with SessionLocal() as session:
            model = session.query(BookingModel).filter(
                BookingModel.customer_id == str(customer_id),
                BookingModel.event_id == str(event_id)
            ).first()
            if model:
                return BookingMapper.to_domain(model)
            return None

    def find_pending_expired(self) -> list[Booking]:
        with SessionLocal() as session:
            models = session.query(BookingModel).filter(BookingModel.status == BookingStatus.PENDING_PAYMENT.value).all()
            return [BookingMapper.to_domain(m) for m in models]

    def save(self, booking: Booking) -> None:
        with SessionLocal() as session:
            model = BookingMapper.to_model(booking)
            session.merge(model)
            session.commit()
    
    def find_by_ticket_code(self, code: TicketCode) -> Booking | None:
        with SessionLocal() as session:
            ticket = session.query(TicketModel).filter(TicketModel.code == code.value).first()
            if ticket:
                model = session.query(BookingModel).filter(BookingModel.id == ticket.booking_id).first()
                if model:
                    return BookingMapper.to_domain(model)
            return None