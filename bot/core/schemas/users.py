from pydantic import BaseModel, Field 
from typing import Optional

class UserCreate(BaseModel):
    id: int

class ShowUserResponse(UserCreate): 
    pass