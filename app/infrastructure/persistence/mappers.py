from uuid import UUID
from decimal import Decimal
from app.domain.shared.value_objects import Money

from app.domain.event.aggregate import Event
from app.domain.event.ticket_category import TicketCategory
from app.domain.event.value_objects import EventStatus

from app.domain.booking.aggregate import Booking
from app.domain.booking.value_objects import BookingId, BookingStatus
from app.domain.ticket.entity import Ticket
from app.domain.ticket.value_objects import TicketId, TicketCode, TicketStatus

from app.domain.refund.aggregate import Refund
from app.domain.refund.value_objects import RefundId, RefundStatus

from app.infrastructure.persistence.models import (
    EventModel, TicketCategoryModel, BookingModel, TicketModel, RefundModel
)

class EventMapper:
    @staticmethod
    def to_domain(model: EventModel) -> Event:
        event = Event(
            name=model.name,
            description=model.description or "",
            start_date=model.start_date,
            end_date=model.end_date,
            location=model.location,
            max_capacity=model.max_capacity
        )
        event.id = UUID(model.id)
        event.status = EventStatus(model.status)
        
        categories = []
        for cat_model in model.categories:
            category = TicketCategory(
                name=cat_model.name,
                price=Money(amount=Decimal(str(cat_model.price_amount)), currency=cat_model.price_currency),
                quota=cat_model.quota,
                sales_start_date=cat_model.sales_start_date,
                sales_end_date=cat_model.sales_end_date
            )
            category.id = UUID(cat_model.id)
            category.is_active = cat_model.is_active
            categories.append(category)
            
        event._ticket_categories = categories
        event.clear_domain_events() # Hapus event creation karena ini memuat data lama
        return event

    @staticmethod
    def to_model(entity: Event) -> EventModel:
        model = EventModel(
            id=str(entity.id),
            name=entity.name,
            description=entity.description,
            start_date=entity.start_date,
            end_date=entity.end_date,
            location=entity.location,
            max_capacity=entity.max_capacity,
            status=entity.status.value
        )
        model.categories = [
            TicketCategoryModel(
                id=str(cat.id),
                event_id=str(entity.id),
                name=cat.name,
                price_amount=float(cat.price.amount),
                price_currency=cat.price.currency,
                quota=cat.quota,
                sales_start_date=cat.sales_start_date,
                sales_end_date=cat.sales_end_date,
                is_active=cat.is_active
            ) for cat in entity.ticket_categories
        ]
        return model

class BookingMapper:
    @staticmethod
    def to_domain(model: BookingModel) -> Booking:
        tickets = []
        for t_model in model.tickets:
            ticket = Ticket(
                id=TicketId(UUID(t_model.id)),
                booking_id=UUID(t_model.booking_id),
                code=TicketCode(t_model.code),
                status=TicketStatus(t_model.status),
                checked_in_at=t_model.checked_in_at
            )
            tickets.append(ticket)

        booking = Booking(
            id=BookingId(UUID(model.id)),
            customer_id=UUID(model.customer_id),
            event_id=UUID(model.event_id),
            category_id=UUID(model.category_id),
            quantity=model.quantity,
            unit_price=Money(amount=Decimal(str(model.total_price_amount / model.quantity)), currency=model.total_price_currency),
            status=BookingStatus(model.status),
            payment_deadline=model.payment_deadline,
            tickets=tickets
        )
        booking.clear_domain_events()
        return booking

    @staticmethod
    def to_model(entity: Booking) -> BookingModel:
        model = BookingModel(
            id=str(entity.id.value),
            customer_id=str(entity.customer_id),
            event_id=str(entity.event_id),
            category_id=str(entity.category_id),
            quantity=entity.quantity,
            total_price_amount=float(entity.total_price.amount),
            total_price_currency=entity.total_price.currency,
            status=entity.status.value,
            payment_deadline=entity.payment_deadline
        )
        model.tickets = [
            TicketModel(
                id=str(t.id.value),
                booking_id=str(entity.id.value),
                code=t.code.value,
                status=t.status.value,
                checked_in_at=t.checked_in_at
            ) for t in entity.tickets
        ]
        return model

class RefundMapper:
    @staticmethod
    def to_domain(model: RefundModel) -> Refund:
        refund = Refund(
            id=RefundId(UUID(model.id)),
            booking_id=UUID(model.booking_id),
            customer_id=UUID(model.customer_id),
            amount=Money(amount=Decimal(str(model.amount)), currency="IDR"),
            status=RefundStatus(model.status),
            reason=model.reason,
            rejection_reason=model.rejection_reason,
            payment_reference=model.payment_reference,
            requested_at=model.requested_at
        )
        refund.clear_domain_events()
        return refund

    @staticmethod
    def to_model(entity: Refund) -> RefundModel:
        return RefundModel(
            id=str(entity.id.value),
            booking_id=str(entity.booking_id),
            customer_id=str(entity.customer_id),
            amount=float(entity.amount),
            status=entity.status.value,
            reason=entity.reason,
            rejection_reason=entity.rejection_reason,
            payment_reference=entity.payment_reference,
            requested_at=entity.requested_at
        )