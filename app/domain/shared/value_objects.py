from dataclasses import dataclass
from decimal import Decimal
from app.domain.shared.errors import DomainError

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "IDR"

    def __post_init__(self):
        if self.amount < 0:
            raise DomainError("Amount cannot be negative")
    
    def is_negative(self) -> bool:
        return self.amount < 0