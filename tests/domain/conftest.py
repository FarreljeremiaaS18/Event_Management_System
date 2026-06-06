import pytest
from decimal import Decimal
from uuid import uuid4

from app.domain.booking.aggregate import Booking
from app.domain.booking.value_objects import BookingStatus
from app.domain.shared.value_objects import Money

def make_money(amount: str = "100000") -> Money:
    return Money(amount=Decimal(amount), currency="IDR")


def make_booking(quantity: int = 2, unit_price=None) -> Booking:
    if unit_price is None:
        unit_price = make_money()
    return Booking.create(
        customer_id=uuid4(),
        event_id=uuid4(),
        category_id=uuid4(),
        quantity=quantity,
        unit_price=unit_price,
    )


def make_paid_booking(quantity: int = 2, unit_price=None) -> Booking:
    booking = make_booking(quantity=quantity, unit_price=unit_price)
    booking.pay(booking.total_price)
    return booking
