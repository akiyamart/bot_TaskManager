from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from ..tools.decorators import db_session_decorator
from ..states import Assistant
from ..ui import menu, skip_description, back_to_menu
from ..api import chat_gpt_session, prompt

router = Router()

@router.callback_query(F.data == "add_task")
@db_session_decorator
async def create_tasks_handler(callback_query: CallbackQuery, db: AsyncSession, state: FSMContext):
    await state.set_state(Assistant.task_manager)
    await callback_query.message.answer(
        "В этом режиме я буду записывать и структурировать твоё расписание\n\nПожалуйста, опиши что тебе нужно ✍️",
        reply_markup=back_to_menu()
    )

@router.message(Assistant.task_manager)
async def AI_assistant_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])

    user_message = message.text
    history.append({"role": "user", "content": user_message})

    try:
        system_prompt = prompt.get_prompt("assistant_task_manager")

        response = await chat_gpt_session.chat_gpt_session_text(messages=history, system_prompt=system_prompt)
        assistant_message = response['choices'][0]['message']['content']

        history.append({"role": "assistant", "content": assistant_message})
        await state.update_data(history=history)
        
        await message.answer(assistant_message)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}\n\n{user_message}\n\n")
