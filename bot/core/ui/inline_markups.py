from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def menu():
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "✍️ Добавление задачи", "callback_data": "add_task"},
        {"text": "📋 Просмотр списка задач", "callback_data": "search_tasks"},
        {"text": "🔎 Просмотр одной задачи", "callback_data": "search_one_task"},
        {"text": "📊 Моя статистика", "callback_data": "search_statistic"},
        {"text": "🤖 Общение с ИИ", "callback_data": "talk_with_AI"},
        {"text": "ℹ️ О боте", "callback_data": "info"}
    ]

    for button in buttons: 
        builder.add(
            InlineKeyboardButton(**button)
        )
    
    builder.adjust(1, 2, 2, 1)

    return builder.as_markup()

def back_to_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👈 Вернуться в меню", callback_data="menu")
            ]
        ]
    )

def skip_description(): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👈 Пропустить ", callback_data="skip_description")
            ]
        ]
    )