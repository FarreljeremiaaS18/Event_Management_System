from uuid import UUID, uuid4
from datetime import datetime
from app.domain.shared.value_objects import Money
from app.domain.shared.errors import DomainError

class TicketCategory:
    def __init__(
            self,
            name: str,
            price: Money,
            quota: int,
            sales_start_date: datetime,
            sales_end_date: datetime,
    ):
        if quota <= 0:
            raise DomainError("Quota must be greater than zero")
        
        if sales_end_date <= sales_start_date:
            raise DomainError("Sales end date must be after sales start date")
        
        self.id: UUID = uuid4()
        self.name: str = name
        self.price: Money = price
        self.quota: int = quota
        self.sales_start_date = sales_start_date
        self.sales_end_date = sales_end_date
        self.is_active = True
    
    def disable(self):
        self.is_active = False
            
        