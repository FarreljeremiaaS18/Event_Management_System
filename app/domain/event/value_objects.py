from enum import Enum

class EventStatus(Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    CANCELED = "Canceled"
    COMPLETED = "Completed"