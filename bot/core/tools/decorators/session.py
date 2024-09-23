from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from functools import wraps
from aiogram.types import CallbackQuery, Message

from ...settings.config import Config

engine = create_async_engine(Config.DATABASE, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

def db_session_decorator(handler):
    @wraps(handler)
    async def wrapper(invoice: Message | CallbackQuery, *args, **kwargs):
        async with async_session() as session:
            try:
                return await handler(invoice, db=session, *args, **kwargs)
            except Exception as e:
                print(f"Error: {e}")
                raise
    return wrapper