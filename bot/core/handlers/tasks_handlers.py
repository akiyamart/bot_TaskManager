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
from ..ui import tasks_back_to_menu, back_to_menu
from ..api import chat_gpt_session, prompt

router = Router()

@router.callback_query(F.data == "add_task")
async def create_tasks_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Assistant.task_manager)
    await callback_query.message.answer(
        "В этом режиме я буду записывать и структурировать твоё расписание\n\nПожалуйста, опиши что тебе нужно ✍️",
        reply_markup=back_to_menu()
    )
    await callback_query.answer()

@router.message(Assistant.task_manager)
@db_session_decorator
async def AI_assistant_handler(message: Message, state: FSMContext, db: AsyncSession):
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

    system_prompt = prompt.get_prompt("assistant_task_manager")
    response = await chat_gpt_session.chat_gpt_session_text(messages=history, system_prompt=system_prompt)
    raw_content = response['choices'][0]['message']['content']

    parser = AIResponseParser(raw_content)
    parser.parse()

    task_data = parser.get_task_data(user_id=message.from_user.id)

    emoji = parser.get_emoji()
    
    task_create_schema = TaskCreate(
        user_id=message.from_user.id,
        title=task_data['title'],
        description=task_data['description'],
        due_date=task_data['due_date'],
        end_time=task_data['end_time'],
    )

    new_task = await create_new_task_service(
        task_create_schema, db
    )
    task_id = new_task.id
    
    message_to_user = (
        f"{emoji} Задача успешно изменена!\n\n"
        f"Название: {new_task.title}\n"
        f"Описание: {new_task.description}\n"
        f"Время начала: {new_task.due_date.strftime('%Y-%m-%d %H:%M')}\n"
        f"Время окончания: {new_task.end_time.strftime('%Y-%m-%d %H:%M')}"
    )

    if task_data['intersection']:
        message_to_user += "\n\n⚠️ Осторожно, в твоём расписании есть пересечение с другими задачами."

    await message.answer(text=message_to_user, reply_markup=tasks_back_to_menu(task_id=task_id))

@router.callback_query(F.data.startswith("delete_task_"))
@db_session_decorator
async def delete_task_handler(callback_query: CallbackQuery, db: AsyncSession):
    task_id = int(callback_query.data.split("_")[2])
    await delete_task_service(task_id=task_id, db=db) 
    await callback_query.answer()

    await callback_query.message.edit_text(
        f"🗑️ Задача успешно удалена!",
        reply_markup=back_to_menu()  
    )
    

@router.callback_query(F.data.startswith("edit_task_"))
async def edit_task_handler(callback_query: CallbackQuery, state: FSMContext):
    task_id = int(callback_query.data.split("_")[2])

    await state.clear()
    await state.set_state(Assistant.edit_task)
    await state.update_data(task_id=task_id)
    await callback_query.answer()

    await callback_query.message.answer(
        "Пожалуйста, укажите новые данные для редактирования задачи 🔧"
    )

@router.message(Assistant.edit_task)
@db_session_decorator
async def process_edit_task(message: Message, state: FSMContext, db: AsyncSession):
    data = await state.get_data()
    task_id = data.get("task_id")

    try:
        tasks = await get_user_tasks_service(user_id=message.from_user.id, db=db)
        current_task = next((task for task in tasks if task.id == task_id), None)

        if not current_task:
            await message.answer("Не удалось найти задачу для редактирования")
            return
    except Exception as e:
        print(f"Ошибка при получении задач: {str(e)}")
        await message.answer("Произошла ошибка при получении задачи")
        return

    user_data = (
        message.text
        + f"\n\nРедактируемая задача: {current_task.title}, {current_task.description}, {current_task.due_date.strftime('%Y-%m-%d %H:%M')}, {current_task.end_time.strftime('%Y-%m-%d %H:%M')}"
    )

    system_prompt = prompt.get_prompt("assistant_task_manager_edit_task")
    response = await chat_gpt_session.chat_gpt_session_text(
        messages=[{"role": "user", "content": user_data}],
        system_prompt=system_prompt
    )
    raw_content = response['choices'][0]['message']['content']
    
    parser = AIResponseParser(raw_content)
    parser.parse()

    task_data = parser.get_task_data(user_id=message.from_user.id)
    emoji = parser.get_emoji()

    task_create_schema = TaskUpdate(
        user_id=message.from_user.id,
        title=task_data['title'],
        description=task_data['description'],
        due_date=task_data['due_date'],
        end_time=task_data['end_time'],
    )

    updated_task = await update_task_service(task_id=task_id, body=task_create_schema, db=db)

    message_to_user = (
        f"{emoji} Задача успешно изменена!\n\n"
        f"Название: {updated_task.title}\n"
        f"Описание: {updated_task.description}\n"
        f"Время начала: {updated_task.due_date.strftime('%Y-%m-%d %H:%M')}\n"
        f"Время окончания: {updated_task.end_time.strftime('%Y-%m-%d %H:%M')}"
    )

    if task_data['intersection']:
        message_to_user += "\n\n⚠️ Осторожно, в твоём расписании есть пересечение с другими задачами."

    await message.answer(text=message_to_user, reply_markup=tasks_back_to_menu(task_id=task_id))
