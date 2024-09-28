from datetime import datetime, timedelta
import uuid 
from typing import Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    due_date: datetime
    start_time: datetime = Field(default=None)
    end_time: datetime = Field(default=None)
    reminder_time: datetime = Field(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        if self.end_time is None:
            self.end_time = self.due_date + timedelta(minutes=30)

class ShowTaskResponse(TaskCreate):
    id: uuid.UUID 

class TaskUpdate(TaskCreate): 
    pass