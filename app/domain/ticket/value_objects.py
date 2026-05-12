from uuid import UUID, uuid4
from enum import Enum


class TicketId:
    def __init__(self, value: UUID):
        self.value = value

    @classmethod
    def generate(cls) -> "TicketId":
        return cls(uuid4())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TicketId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"TicketId({self.value})"


class TicketCode:
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def generate(cls) -> "TicketCode":
        return cls(str(uuid4()).replace("-", "").upper())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TicketCode):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"TicketCode({self.value})"


class TicketStatus(Enum):
    ACTIVE = "Active"
    CHECKED_IN = "CheckedIn"
    CANCELLED = "Cancelled"