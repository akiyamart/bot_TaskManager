import os

from aiogram import Bot, Dispatcher

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    DATABASE = os.getenv("DATABASE_DSN", "")
    # BOT_TOKEN = os.getenv("BOT_TOKEN", "")

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()