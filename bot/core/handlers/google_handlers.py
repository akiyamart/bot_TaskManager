import io
import json
from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from sqlalchemy.ext.asyncio import AsyncSession

from ..tools.decorators import db_session_decorator, check_user_decorator
from ..tools.services import update_google_oauth_data, delete_google_oauth_data
from ..ui import google_oauth, back_to_menu
from ..states import Assistant
from ..schemas import ShowUserResponse, GoogleOAuthCreate, GoogleOAuthDelete, ShowGoogleOAuthResponse

router = Router()

@router.callback_query(F.data == "google_sync")
async def google_handler(callback_query: CallbackQuery, state: FSMContext): 
    await callback_query.answer()
    await state.set_state(Assistant.google_oauth)
    if hasattr(callback_query, "data"): 
        message = callback_query.message
    else: 
        message = callback_query
    await message.answer(
        text="Вышлите файл формата .json",
        reply_markup=google_oauth()
    )

@router.callback_query(F.data == "google_sync_delete")
@db_session_decorator
@check_user_decorator
async def google_delete_handler(callback_query: CallbackQuery, db: AsyncSession, user: ShowUserResponse, state: FSMContext):
    await callback_query.answer() 
    result = await delete_google_oauth_data(
        GoogleOAuthDelete(user_id=user.id), db=db
    )
    if isinstance(result, ShowGoogleOAuthResponse):
        await callback_query.message.answer("Данные успешно удалены!", reply_markup=back_to_menu())
    else:
        await callback_query.message.answer("Данные в базе не найдены!", reply_markup=back_to_menu())


@router.message(Assistant.google_oauth)
@db_session_decorator
@check_user_decorator
async def google_document_handler(message: Message, db: AsyncSession, user: ShowUserResponse, state: FSMContext): 
    if message.document.mime_type != 'application/json':
        return await message.answer(
            text="Вышлите файл формата .json",
            reply_markup=google_oauth()
        )

    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path

    json_file = io.BytesIO()  
    await message.bot.download_file(file_path, json_file)
    
    try:
        json_data = json.load(json_file)  

        data = await update_google_oauth_data(
            GoogleOAuthCreate(
                user_id=user.id,
                project_id=json_data['project_id'],
                private_key_id=json_data['private_key_id'],
                private_key=json_data['private_key'],
                client_email=json_data['client_email'],
                client_id=json_data['client_id'],
                auth_uri=json_data['auth_uri'],
                token_uri=json_data['token_uri'],
                auth_provider_x509_cert_url=json_data['auth_provider_x509_cert_url'],
                client_x509_cert_url=json_data['client_x509_cert_url'],
                universe_domain=json_data['universe_domain'],
            ), db=db
        )

        if isinstance(data, ShowGoogleOAuthResponse):
            await message.answer("Данные добавлены успешно!", reply_markup=back_to_menu())

        else:
            await message.answer("Что-то пошло не так. Попытайтесь ещё раз!")

    except json.JSONDecodeError:
        await message.answer("Ошибка: файл не является корректным JSON.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке файла: {str(e)}")