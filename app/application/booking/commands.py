from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

@dataclass(frozen=True)
class PayBookingCommand:
    booking_id: UUID
    payment_amount: Decimal

@dataclass(frozen=True)
class BookingDTO:
    booking_id: UUID
    status: str