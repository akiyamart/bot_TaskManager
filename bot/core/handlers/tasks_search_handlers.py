from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from ..tools.decorators import db_session_decorator
from ..settings import bot
from ..tools.services import create_new_task_service, get_user_tasks_service, delete_task_service, update_task_service
from ..tools.classes import AIResponseParser
from ..schemas import TaskCreate, TaskUpdate
from ..states import Assistant
from ..ui import menu, tasks_back_to_menu, back_to_menu
from ..api import chat_gpt_session, prompt

router = Router()

@router.callback_query(F.data == "search_tasks")
async def start_search_tasks_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Assistant.search_tasks)
    await callback_query.message.answer(
        "В этом режиме я помогу тебе найти твои задачи 😌\n\nПожалуйста, опиши, что тебе нужно  🔍",
        reply_markup=back_to_menu()
    )
    await callback_query.answer()

@router.message(Assistant.search_tasks)
@db_session_decorator
async def search_tasks_handler(message: Message, db: AsyncSession, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])

    await bot.send_chat_action(message.chat.id, action="typing")

    if not history:
        try:
            tasks = await get_user_tasks_service(user_id=message.from_user.id, db=db)
            tasks_info = ""
            if tasks:
                tasks_info = "\n".join(
                    [f"-\n{task.title}:\n{task.description}\n\n(Срок: {task.due_date.strftime('%Y-%m-%d %H:%M')})\n\n(Окончание задачи: {task.end_time.strftime('%Y-%m-%d %H:%M')})" for task in tasks]
                )
            else:
                tasks_info = ""
        except Exception as e:
            print(f"Ошибка при получении задач: {str(e)}")
            tasks_info = "Не удалось получить текущие задачи."
    else:
        tasks_info = ""

    user_data = (
        message.text + f"\n\nСегодняшняя дата: {datetime.now()}" + f"\n\nВсе задачи пользователя:\n{tasks_info}"
    )
    history.append({"role": "user", "content": user_data})
    await state.update_data(history=history)

    system_prompt = prompt.get_prompt("assistant_task_manager_search")
    response = await chat_gpt_session.chat_gpt_session_text(messages=history, system_prompt=system_prompt)

    content = response['choices'][0]['message']['content']
    await message.answer(text=content, reply_markup=back_to_menu())
