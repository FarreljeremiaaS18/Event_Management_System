from app.infrastructure.persistence.event_repository import EventRepository
from app.infrastructure.persistence.booking_repository import BookingRepository
from app.infrastructure.persistence.ticket_repository import TicketRepository
from app.infrastructure.persistence.refund_repository import RefundRepository
from app.infrastructure.services.payment_gateway import PaymentGateway
from app.infrastructure.services.refund_payment_service import RefundPaymentService

from app.application.event.handlers import CreateEventCommandHandler
from app.application.booking.handlers import CreateBookingCommandHandler, PayBookingCommandHandler
from app.application.ticket.handlers import CheckInTicketCommandHandler
from app.application.refund.handlers import MarkRefundPaidOutCommandHandler

event_repository = EventRepository()
booking_repository = BookingRepository()
ticket_repository = TicketRepository()
refund_repository = RefundRepository()
payment_gateway = PaymentGateway()
refund_payment_service = RefundPaymentService()

def get_create_event_handler() -> CreateEventCommandHandler:
  
    return CreateEventCommandHandler(event_repository=event_repository)

def get_create_booking_handler() -> CreateBookingCommandHandler:
    return CreateBookingCommandHandler(repository=booking_repository)

def get_pay_booking_handler() -> PayBookingCommandHandler:
    return PayBookingCommandHandler(
        booking_repository=booking_repository,
        payment_gateway=payment_gateway
    )

def get_check_in_ticket_handler() -> CheckInTicketCommandHandler:
    return CheckInTicketCommandHandler(repository=ticket_repository)

def get_mark_refund_paid_out_handler() -> MarkRefundPaidOutCommandHandler:
    return MarkRefundPaidOutCommandHandler(
        repository=refund_repository,
        payout_service=refund_payment_service
    )