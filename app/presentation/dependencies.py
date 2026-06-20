from app.infrastructure.persistence.event_repository import EventRepository
from app.infrastructure.persistence.booking_repository import BookingRepository
from app.infrastructure.services.payment_gateway import PaymentGateway
from app.application.event.handlers import CreateEventCommandHandler
from app.application.booking.handlers import CreateBookingCommandHandler, PayBookingCommandHandler


event_repository = EventRepository()
booking_repository = BookingRepository()
payment_gateway = PaymentGateway()

def get_create_event_handler() -> CreateEventCommandHandler:
  
    return CreateEventCommandHandler(event_repository=event_repository)

def get_create_booking_handler() -> CreateBookingCommandHandler:
    return CreateBookingCommandHandler(repository=booking_repository)

def get_pay_booking_handler() -> PayBookingCommandHandler:
    return PayBookingCommandHandler(
        booking_repository=booking_repository,
        payment_gateway=payment_gateway
    )