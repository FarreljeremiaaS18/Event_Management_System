from datetime import datetime, UTC
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class DomainEvent(BaseModel):
    evemt_id: UUID = Field(default_factory=uuid4)

    occurred_on: datetime = Field(default_factory=lambda: datetime.now(UTC))