from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..tools.classes import Cycle

def menu():
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "✍️ Добавление задачи", "callback_data": "add_task"},
        {"text": "📋 Просмотр списка задач", "callback_data": "search_tasks"},
        {"text": "🔎 Просмотр одной задачи", "callback_data": "list_tasks"},
        {"text": "📊 Моя статистика", "callback_data": "get_statistics"},
        {"text": "🤖 Общение с ИИ", "callback_data": "talk_with_AI"},
        {"text": "📅 Синхронизация с Google Calendar", "callback_data": "google_sync"},
    ]

    for button in buttons: 
        builder.add(
            InlineKeyboardButton(**button)
        )
    
    builder.adjust(1, 2, 2, 1)

    return builder.as_markup()

def google_oauth():
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "🗑️ Отвязать google calendar", "callback_data": "google_sync_delete"},
        {"text": '👈 Вернуться в меню', "callback_data": "menu"}
    ]

    for button in buttons: 
        builder.add(
            InlineKeyboardButton(**button)
        )
    
    builder.adjust(1, 1)

    return builder.as_markup()
    

def back_to_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👈 Вернуться в меню", callback_data="menu")
            ]
        ]
    )

def tasks_back_to_menu(task_id: int): 
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "🔧 Редактировать", "callback_data": f"edit_task_{task_id}"},
        {"text": "❌ Удалить", "callback_data": f"delete_task_{task_id}"},
        # {"text": "👈 Вернуться в меню", "callback_data": "menu"},
    ]

    for button in buttons: 
        builder.add(
            InlineKeyboardButton(**button)
        )
    
    builder.adjust(2)

    return builder.as_markup()

def scroll_keyboard(iterable: Cycle, task_id: id):
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "⬅️", "callback_data": "-1"},
        {"text": "➡️", "callback_data": "1"},
        {"text": "🔧 Редактировать", "callback_data": f"edit_task_{task_id}"},
        {"text": "❌ Удалить", "callback_data": f"delete_task_{task_id}"},
        {"text": "👈 Вернуться в меню", "callback_data": "menu"},
    ]


    if len(iterable) == 1:
        buttons[0] = {"text": " ", "callback_data": "_"} 
        buttons[1] = {"text": " ", "callback_data": "_"}  

    for button in buttons:
        builder.add(
            InlineKeyboardButton(**button)
        )

    builder.adjust(2, 2, 1) 
    return builder.as_markup()
