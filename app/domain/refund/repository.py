from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.refund.aggregate import Refund


class IRefundRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: UUID) -> Refund | None: ...

    @abstractmethod
    def find_by_booking(self, booking_id: UUID) -> Refund | None:
        ...

    @abstractmethod
    def save(self, refund: Refund) -> None: ...