from uuid import UUID
from app.domain.shared.domain_event import DomainEvent


class RefundRequested(DomainEvent): # BR28, BR29
    refund_id_ref: UUID
    booking_id_ref: UUID
    customer_id_ref: UUID

 
class RefundApproved(DomainEvent): # BR32
    refund_id_ref: UUID
    booking_id_ref: UUID


class RefundRejected(DomainEvent): # BR33
    refund_id_ref: UUID
    booking_id_ref: UUID
    rejection_reason: str


class RefundPaidOut(DomainEvent): # BR34
    refund_id_ref: UUID
    booking_id_ref: UUID
    payment_reference: str