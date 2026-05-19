from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class RequestRefundCommand:
    booking_id: UUID
    customer_id: UUID

@dataclass(frozen=True)
class ApproveRefundCommand:
    refund_id: UUID

@dataclass(frozen=True)
class RejectRefundCommand:
    refund_id: UUID
    reason: str

@dataclass(frozen=True)
class MarkRefundPaidOutCommand:
    refund_id: UUID
    payment_reference: str