from aiogram import Dispatcher

from ..handlers import main_router, tasks_router, google_router, search_router, list_router

def dp_setting(dp: Dispatcher) -> None: 
    dp.include_router(main_router)
    dp.include_router(tasks_router)
    dp.include_router(google_router)
    dp.include_router(search_router)
    dp.include_router(list_router)
