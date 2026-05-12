from uuid import UUID, uuid4
from enum import Enum


class RefundId:
    def __init__(self, value: UUID):
        self.value = value

    @classmethod
    def generate(cls) -> "RefundId":
        return cls(uuid4())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RefundId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"RefundId({self.value})"


class RefundStatus(Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID_OUT = "PaidOut"