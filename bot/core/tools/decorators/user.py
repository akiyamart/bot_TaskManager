from sqlalchemy.ext.asyncio import async_sessionmaker

from functools import wraps
from aiogram.types import CallbackQuery, Message

from ...schemas import UserCreate

from ..services import get_user

def check_user_decorator(handler):
    @wraps(handler)
    async def wrapper(invoice: Message | CallbackQuery, db: async_sessionmaker, *args, **kwargs):
        try:
            id = invoice.from_user.id
            user = await get_user(UserCreate(
                id=id,
            ), db=db)
            return await handler(invoice, db=db, user=user, *args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            raise
    return wrapper