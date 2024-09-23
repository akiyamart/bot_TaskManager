from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from typing import Union, Dict

from ..models import User

class UserDAL:
    def __init__(self, db_connect: AsyncSession):
        self.db_connect = db_connect

    async def create_user(self, id: int) -> User:
        new_user = User(
            id=id
        )
        self.db_connect.add(new_user)
        await self.db_connect.flush()
        return new_user

    async def get_user(self, id: int) -> User:
        stmt = select(User).where(User.id == id)
        result = await self.db_connect.execute(stmt)
        return result.scalars().first()