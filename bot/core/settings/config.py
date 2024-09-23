import os

from aiogram import Bot, Dispatcher

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", '7670322043:AAHw-6_DIFO2v-R47oBUcn3MC81jOO-xZHU')
    DATABASE = os.getenv("DATABASE_DSN", "postgresql+asyncpg://postgres:holdmn@localhost:5436/task_manager_postgres")
    # BOT_TOKEN = os.getenv("BOT_TOKEN", "6676724790:AAEvd6ofLoMiAJ8ks1YvR1I2jhmSg9n1vMw")

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()