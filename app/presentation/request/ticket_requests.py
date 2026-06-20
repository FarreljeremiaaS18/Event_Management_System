from pydantic import BaseModel
from uuid import UUID

class CheckInRequest(BaseModel):
    event_id: UUID