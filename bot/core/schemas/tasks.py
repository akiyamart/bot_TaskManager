from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    due_date: datetime
    end_time: datetime = Field(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        if self.end_time is None:
            self.end_time = self.due_date + timedelta(minutes=30)

class ShowTaskResponse(TaskCreate):
    id: int 

class TaskUpdate(TaskCreate): 
    pass