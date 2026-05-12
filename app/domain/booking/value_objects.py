from uuid import UUID, uuid4
from enum import Enum


class BookingId:
    def __init__(self, value: UUID):
        self.value = value

    @classmethod
    def generate(cls) -> "BookingId":
        return cls(uuid4())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BookingId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"BookingId({self.value})"


class BookingStatus(Enum):
    PENDING_PAYMENT = "PendingPayment"
    PAID = "Paid"
    EXPIRED = "Expired"
    REFUNDED = "Refunded"