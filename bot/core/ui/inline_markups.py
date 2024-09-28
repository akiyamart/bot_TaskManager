from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .cycle import Cycle

def menu():
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "📋 Cписок", "callback_data": "list_tasks"},
        {"text": "📊 Статистика", "callback_data": "get_statistics"},
        {"text": "📅 Синхронизация с Google Calendar", "callback_data": "google_sync"},
    ]

    for button in buttons: 
        builder.add(
            InlineKeyboardButton(**button)
        )
    
    builder.adjust(1, 1, 1)

    return builder.as_markup()

def google_oauth():
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "🗑️ Отвязать Google Calendar", "callback_data": "google_sync_delete"},
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

def start_to_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="▶️ Приступить к работе", callback_data="menu")
            ]
        ]
    )


def scroll_keyboard(iterable: Cycle, task_id: id):
    builder = InlineKeyboardBuilder()

    buttons = [
        {"text": "⬅️", "callback_data": "-1"},
        {"text": "➡️", "callback_data": "1"},
        {"text": "👈 Вернуться в меню", "callback_data": "menu"},
    ]


    if len(iterable) == 1:
        buttons[0] = {"text": " ", "callback_data": "_"} 
        buttons[1] = {"text": " ", "callback_data": "_"}  

    for button in buttons:
        builder.add(
            InlineKeyboardButton(**button)
        )

    builder.adjust(2, 1) 
    return builder.as_markup()
