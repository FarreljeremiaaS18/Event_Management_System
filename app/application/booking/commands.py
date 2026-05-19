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

@dataclass(frozen=True)
class CreateBookingCommand:
    customer_id: UUID
    event_id: UUID
    category_id: UUID
    quantity: int
    unit_price: Decimal

@dataclass(frozen=True)
class ExpireBookingCommand:
    booking_id: UUID