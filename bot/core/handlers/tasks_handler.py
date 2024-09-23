from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..tools.decorators import db_session_decorator
from ..ui import menu, skip_description
from ..schemas import TaskCreate
from ..tools.services import create_new_task

router = Router()

@router.callback_query(F.data == "add_task")
@db_session_decorator
async def create_tasks_handler(callback_query: CallbackQuery, db: AsyncSession, state: FSMContext):
    # Добавить декоратор проверки пользователя
    pass