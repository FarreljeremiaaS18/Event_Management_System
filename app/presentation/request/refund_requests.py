from pydantic import BaseModel

class MarkPaidOutRequest(BaseModel):
    payment_reference: str