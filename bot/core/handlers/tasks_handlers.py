from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from datetime import datetime

from ..tools.decorators import db_session_decorator
from ..settings import bot
from ..tools.services import get_user_tasks_service
from ..states import Assistant
from ..api import chat_gpt_session, prompt
from ..tools.classes import AIResponseHandler, ScheduleManager

router = Router()
scheduler = ScheduleManager(bot)

@router.message(Assistant.task_manager)
@db_session_decorator
async def AI_assistant_handler(message: Message, state: FSMContext, db: AsyncSession):
    data = await state.get_data()
    history = data.get("history", [])
    await bot.send_chat_action(message.chat.id, action="typing")

    tasks_info = ""
    try:
        tasks = await get_user_tasks_service(user_id=message.from_user.id, db=db)
        if tasks:
            tasks_info = "\n".join(
                [
                    f"-\nUUID_task: {task.id}\n"
                    f"Заголовок: {task.title}:\n"
                    f"Описание: {task.description}\n"
                    f"Число задачи: {task.due_date.strftime('%Y-%m-%d %H:%M')}\n"
                    f"Время начала задачи: {task.start_time.strftime('%Y-%m-%d %H:%M')}"
                    f"Время окончания задачи: {task.end_time.strftime('%Y-%m-%d %H:%M')}"
                    f"Время напоминания: {task.reminder_time.strftime('%Y-%m-%d %H:%M')}"
                    for task in tasks
                ]
            )
    except Exception as e:
        tasks_info = f"У пользователя нет задач, {e}"
    
    user_data = (
        message.text + f"\n\nСегодняшняя дата: {datetime.now()}" + f"\n\nВсе задачи пользователя:\n{tasks_info}"
    )
    
    history.append({"role": "user", "content": user_data})

    system_prompt = prompt.get_prompt("assistant_task_manager")
    response = await chat_gpt_session.chat_gpt_session_text(messages=history, system_prompt=system_prompt)
    raw_content = response['choices'][0]['message']['content']
    print(raw_content)
    handler = AIResponseHandler(raw_content=raw_content, user_id=message.from_user.id, db_session=db)
    await handler.handle_response(message)

    if task_data := handler.parser.get_event_data(user_id=message.from_user.id):
        print(task_data)
        if task_data.get('code') == "1" or task_data.get('code') == "2":
            reminder_time_str = task_data.get('reminder')
            reminder_time = datetime.strptime(reminder_time_str, '%H:%M')

            text_to_user = (
                        f"⏰ Напоминание о задаче!\n\nНазвание: {task_data.get('title')}\n"
                        f"Описание: {task_data.get('description')}\nВремя начала: {task_data.get('start_time')}\n"
                        f"Время окончания: {task_data.get('end_time')}\n"
            )

            await scheduler.schedule_reminder(
                chat_id=message.from_user.id, reminder_time=reminder_time, message=text_to_user
            )