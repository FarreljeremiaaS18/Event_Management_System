from uuid import UUID
from datetime import datetime, UTC

from app.domain.shared.aggregate_root import AggregateRoot
from app.domain.shared.errors import DomainError
from app.domain.refund.value_objects import RefundId, RefundStatus
from app.domain.refund.events import (
    RefundRequested,
    RefundApproved,
    RefundRejected,
    RefundPaidOut,
)


class Refund(AggregateRoot):
    def __init__(
        self,
        id: RefundId,
        booking_id: UUID,
        customer_id: UUID,
        amount,
        status: RefundStatus,
        reason: str | None = None,
        rejection_reason: str | None = None,
        payment_reference: str | None = None,
        requested_at: datetime | None = None,
    ):
        super().__init__()
        self.id = id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount
        self.status = status
        self.reason = reason
        self.rejection_reason = rejection_reason
        self.payment_reference = payment_reference
        self.requested_at = requested_at or datetime.now(UTC)

    @classmethod
    def request(
        cls,
        booking_id: UUID,
        customer_id: UUID,
        amount,
        reason: str | None = None,
    ) -> "Refund":
        refund = cls(
            id=RefundId.generate(),
            booking_id=booking_id,
            customer_id=customer_id,
            amount=amount,
            status=RefundStatus.REQUESTED,
            reason=reason,
        )
        refund.add_domain_event(
            RefundRequested(
                refund_id_ref=refund.id.value,
                booking_id_ref=booking_id,
                customer_id_ref=customer_id,
            )
        )
        return refund

    def approve(self) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise DomainError("Only a requested refund can be approved")

        self.status = RefundStatus.APPROVED
        self.add_domain_event(
            RefundApproved(
                refund_id_ref=self.id.value,
                booking_id_ref=self.booking_id,
            )
        )

    def reject(self, rejection_reason: str) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise DomainError("Only a requested refund can be rejected")
        if not rejection_reason or not rejection_reason.strip():
            raise DomainError("Rejection reason must be provided")  # BR31

        self.status = RefundStatus.REJECTED
        self.rejection_reason = rejection_reason
        self.add_domain_event(
            RefundRejected(
                refund_id_ref=self.id.value,
                booking_id_ref=self.booking_id,
                rejection_reason=rejection_reason,
            )
        )

    def mark_paid_out(self, payment_reference: str) -> None:
        if self.status == RefundStatus.PAID_OUT:
            raise DomainError("Refund has already been paid out")  # BR34
        if self.status != RefundStatus.APPROVED:
            raise DomainError("Only an approved refund can be marked as paid out")
        if not payment_reference or not payment_reference.strip():
            raise DomainError("Payment reference must be provided")  # BR34

        self.status = RefundStatus.PAID_OUT
        self.payment_reference = payment_reference
        self.add_domain_event(
            RefundPaidOut(
                refund_id_ref=self.id.value,
                booking_id_ref=self.booking_id,
                payment_reference=payment_reference,
            )
        )