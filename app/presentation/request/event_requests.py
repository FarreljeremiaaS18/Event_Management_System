from pydantic import BaseModel
from datetime import datetime

class CreateEventRequest(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    max_capacity: int