from uuid import UUID

from app.domain.refund.aggregate import Refund
from app.domain.refund.repository import IRefundRepository


class RefundRepository(IRefundRepository):
    def __init__(self):
        self._refunds: dict[UUID, Refund] = {}

    def find_by_id(self, id: UUID) -> Refund | None:
        return self._refunds.get(id)

    def find_by_booking(self, booking_id: UUID) -> Refund | None:
        for refund in self._refunds.values():
            if refund.booking_id == booking_id:
                return refund

        return None

    def save(self, refund: Refund) -> None:
        self._refunds[refund.id.value] = refund