import pytest
from uuid import uuid4

from app.domain.shared.errors import DomainError
from app.domain.refund.aggregate import Refund
from app.domain.refund.value_objects import RefundStatus
from app.domain.refund.events import (
    RefundRequested,
    RefundApproved,
    RefundRejected,
)


class TestRefundCreation:

    def test_request_refund_creates_requested_refund(self):
        refund = Refund.request(
            booking_id=uuid4(),
            customer_id=uuid4(),
            amount=100000,
            reason="Cannot attend event"
        )

        assert refund.status == RefundStatus.REQUESTED
        assert refund.reason == "Cannot attend event"
        assert len(refund.domain_events) == 1
        assert isinstance(refund.domain_events[0], RefundRequested)


class TestRefundApproval:

    def test_approve_requested_refund(self):
        refund = Refund.request(
            booking_id=uuid4(),
            customer_id=uuid4(),
            amount=100000
        )

        refund.approve()

        assert refund.status == RefundStatus.APPROVED
        assert isinstance(refund.domain_events[-1], RefundApproved)

    def test_cannot_approve_non_requested_refund(self):
        refund = Refund.request(
            booking_id=uuid4(),
            customer_id=uuid4(),
            amount=100000
        )

        refund.approve()

        with pytest.raises(DomainError):
            refund.approve()


class TestRefundRejection:

    def test_reject_requested_refund(self):
        refund = Refund.request(
            booking_id=uuid4(),
            customer_id=uuid4(),
            amount=100000
        )

        refund.reject("Event cancelled by organizer")

        assert refund.status == RefundStatus.REJECTED
        assert refund.rejection_reason == "Event cancelled by organizer"
        assert isinstance(refund.domain_events[-1], RefundRejected)

    def test_reject_requires_reason(self):
        refund = Refund.request(
            booking_id=uuid4(),
            customer_id=uuid4(),
            amount=100000
        )

        with pytest.raises(DomainError):
            refund.reject("")

    def test_cannot_reject_after_approval(self):
        refund = Refund.request(
            booking_id=uuid4(),
            customer_id=uuid4(),
            amount=100000
        )

        refund.approve()

        with pytest.raises(DomainError):
            refund.reject("Too late")