from datetime import datetime, UTC
from app.application.booking.commands import PayBookingCommand, BookingDTO
from app.application.interfaces.external_services import IPaymentGateway
from app.domain.booking.repository import IBookingRepository
from app.domain.shared.value_objects import Money

class PayBookingCommandHandler:
    def __init__(self, booking_repository: IBookingRepository, payment_gateway: IPaymentGateway):
        self.repository = booking_repository
        self.payment_gateway = payment_gateway

    def execute(self, command: PayBookingCommand) -> BookingDTO:
        
        booking = self.repository.find_by_id(command.booking_id)
        if not booking:
            raise ValueError("Booking tidak ditemukan")

        payment_success = self.payment_gateway.process_payment(
            booking_id=str(booking.id), 
            amount=float(command.payment_amount)
        )
        
        if not payment_success:
            raise ValueError("Pembayaran ditolak oleh bank")

        uang_dibayar = Money(command.payment_amount)
        booking.pay(uang_dibayar, current_time=datetime.now(UTC))
    
        self.repository.save(booking)
        
        return BookingDTO(booking_id=booking.id, status=booking.status.value)