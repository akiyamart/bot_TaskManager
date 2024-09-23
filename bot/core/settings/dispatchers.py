from aiogram import Dispatcher

from ..handlers import main_router, tasks_router

def dp_setting(dp: Dispatcher) -> None: 
    dp.include_router(main_router)
    dp.include_router(tasks_router)
