import asyncio

from core.settings import bot, dp
from core.commands import set_commands
from core.settings import dp_setting

async def on_startup():
    print("Бот запущен")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    dp.startup.register(on_startup)
    dp_setting(dp)
    try:
        await dp.start_polling(bot)
    finally: 
        await bot.session.close()
    

if __name__ == '__main__':  
    asyncio.run(main())