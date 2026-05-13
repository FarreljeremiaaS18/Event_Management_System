import pytest
from datetime import datetime, timedelta, UTC
from decimal import Decimal
from uuid import uuid4

from app.domain.shared.errors import DomainError
from app.domain.booking.value_objects import BookingStatus
from app.domain.booking.events import BookingCreated, BookingPaid, BookingExpired
from app.domain.ticket.value_objects import TicketStatus
from tests.domain.conftest import make_booking, make_paid_booking, make_money


class TestBookingCreation:

    def test_raises_if_quantity_is_zero(self):
        with pytest.raises(DomainError, match="Quantity"):
            make_booking(quantity=0)

    def test_raises_if_quantity_is_negative(self):
        with pytest.raises(DomainError, match="Quantity"):
            make_booking(quantity=-1)

    def test_status_is_pending_payment_on_creation(self):
        booking = make_booking()
        assert booking.status == BookingStatus.PENDING_PAYMENT

    def test_payment_deadline_is_set_on_creation(self):
        before = datetime.now(UTC)
        booking = make_booking()
        assert booking.payment_deadline > before

    def test_total_price_equals_unit_price_times_quantity(self):
        booking = make_booking(quantity=3, unit_price=make_money("50000"))
        assert booking.total_price.amount == Decimal("150000")

    def test_booking_created_domain_event_is_raised(self):
        booking = make_booking()
        events = booking.collect_events()
        assert any(isinstance(e, BookingCreated) for e in events)


class TestBookingPayment:

    def test_raises_if_amount_does_not_match(self):
        booking = make_booking()
        wrong_amount = make_money("1")
        with pytest.raises(DomainError, match="total price"):
            booking.pay(wrong_amount)

    def test_raises_if_deadline_has_passed(self):
        booking = make_booking()
        booking.payment_deadline = datetime.now(UTC) - timedelta(minutes=1)
        with pytest.raises(DomainError, match="deadline"):
            booking.pay(booking.total_price)

    def test_raises_if_booking_is_expired(self):
        booking = make_booking()
        booking.status = BookingStatus.EXPIRED
        with pytest.raises(DomainError, match="expired"):
            booking.pay(booking.total_price)

    def test_pay_changes_status_to_paid(self):
        booking = make_booking()
        booking.pay(booking.total_price)
        assert booking.status == BookingStatus.PAID

    def test_tickets_are_issued_after_payment(self):
        booking = make_booking(quantity=3)
        booking.pay(booking.total_price)
        assert len(booking.tickets) == 3

    def test_all_issued_tickets_are_active(self):
        booking = make_paid_booking()
        assert all(t.status == TicketStatus.ACTIVE for t in booking.tickets)

    def test_booking_paid_domain_event_is_raised(self):
        booking = make_booking()
        booking.collect_events()
        booking.pay(booking.total_price)
        events = booking.collect_events()
        assert any(isinstance(e, BookingPaid) for e in events)


class TestBookingExpiry:

    def test_raises_if_booking_is_paid(self):
        booking = make_paid_booking()
        with pytest.raises(DomainError, match="paid"):
            booking.expire()

    def test_expire_changes_status_to_expired(self):
        booking = make_booking()
        booking.expire()
        assert booking.status == BookingStatus.EXPIRED

    def test_booking_expired_event_contains_correct_quantity(self):
        booking = make_booking(quantity=4)
        booking.collect_events()
        booking.expire()
        events = booking.collect_events()
        expired_event = next(e for e in events if isinstance(e, BookingExpired))
        assert expired_event.quantity == 4

        def test_expire_is_idempotent_if_already_expired(self):
            booking = make_booking()
            booking.expire()
            booking.expire()
            assert booking.status == BookingStatus.EXPIRED