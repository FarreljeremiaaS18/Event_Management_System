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
    
    def multiply(self, factor: int) -> "Money":
        return Money(amount=self.amount * factor, currency=self.currency)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency
    
    def is_negative(self) -> bool:
        return self.amount < 0