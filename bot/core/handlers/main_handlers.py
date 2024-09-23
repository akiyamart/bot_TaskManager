from aiogram import Router, F 
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession


from ..tools.decorators import db_session_decorator, check_user_decorator
from ..ui import menu, back_to_menu
from ..schemas import ShowUserResponse

router = Router()

@router.message(Command("start"))
@db_session_decorator
@check_user_decorator
async def start_handler(message: Message, db: AsyncSession, user: ShowUserResponse):
    id = message.from_user.id
    username = message.from_user.username

    try:
        print(user)

        await message.answer(text=f"Привет, {username}", reply_markup=menu())

    except Exception as e:
        print(f"Ошибка в start_handler: {e}")
        await message.answer(
            text="Что-то пошло не так, попробуй позже",
        )


@router.callback_query(F.data == "menu")
@router.message(Command("menu"))
async def menu_handler(invoice: Message | CallbackQuery, state: FSMContext): 
    await state.clear()
    if hasattr(invoice, "data"): 
        message = invoice.message
    else: 
        message = invoice
    await message.answer(
        text="Выбери действие ниже 👇",
        reply_markup=menu()
    )
    try: 
        await invoice.message.delete()
    except: 
        pass

@router.callback_query(F.data == "info")
async def info_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text="{Добавить информацию о боте}",
        reply_markup=back_to_menu()
    )
    try:
        await callback_query.message.delete()
    except:
        pass