from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Model(AsyncAttrs, DeclarativeBase): 
    pass