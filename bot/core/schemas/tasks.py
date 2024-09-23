from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default="pending") 
    due_date: Optional[datetime] = Field(default=None)

class ShowTaskResponse(TaskCreate):  
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
