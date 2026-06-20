from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class CreateBookingRequest(BaseModel):
    customer_id: UUID
    event_id: UUID
    category_id: UUID
    quantity: int
    unit_price: Decimal

class PayBookingRequest(BaseModel):
    payment_amount: Decimal