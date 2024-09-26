import os

from aiogram import Bot, Dispatcher

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    DATABASE = os.getenv("DATABASE_DSN", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PROXY_USERNAME = os.getenv("PROXY_USERNAME", "")
    PROXY_PASS = os.getenv("PROXY_PASS", "") 
    PROXY_ENDPOINT = os.getenv("PROXY_ENDPOINT", "") 

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()