from aiogram import Bot
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='/start',
            description='Перезапустить бота'
        ),
        BotCommand(
            command='/menu',
            description='Меню'
        )
    ]
    await bot.set_my_commands(commands)