from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from ..tools.decorators import db_session_decorator
from ..tools.services import get_user_tasks_service
from ..ui import scroll_keyboard
from ..ui.cycle import Cycle

router = Router()

@router.callback_query(F.data == "list_tasks")
@db_session_decorator
async def start_search_tasks_handler(callback_query: CallbackQuery, db: AsyncSession, state: FSMContext):
    tasks = await get_user_tasks_service(user_id=callback_query.from_user.id, db=db)
    
    if not tasks:
        await callback_query.message.answer("Похоже твоих задач нет 🙁")
        return

    tasks_cycle = Cycle(tasks)
    task = tasks_cycle.move(direction=1) 

    output_message = f"🎯\nНазвание: {task.title}\nОписание: {task.description}\nВремя начала: {task.due_date}\nВремя окончания: {task.end_time}\n"
    await callback_query.message.answer(
        text=output_message,
        reply_markup=scroll_keyboard(iterable=tasks_cycle, task_id=task.id),
        parse_mode='html',
        disable_web_page_preview=True
    )

    await state.update_data({"all_tasks": tasks_cycle})

    await callback_query.answer()

@router.callback_query(F.data.in_(["-1", "1"]))
async def scroll_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tasks_cycle: Cycle = data.get("all_tasks")

    task = tasks_cycle.move(int(callback_query.data))

    output_message = f"🎯\nНазвание: {task.title}\nОписание: {task.description}\nВремя начала: {task.due_date}\nВремя окончания: {task.end_time}\n"
    await callback_query.message.edit_text(
        text=output_message,
        reply_markup=scroll_keyboard(iterable=tasks_cycle, task_id=task.id),
        parse_mode='html',
        disable_web_page_preview=True
    )

    await callback_query.answer()
