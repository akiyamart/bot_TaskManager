import aioschedule as schedule
from aiogram import Bot
from datetime import datetime
import asyncio

class ScheduleManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.jobs = {}

    async def send_reminder(self, chat_id, message):
        await self.bot.send_message(chat_id, message)

    async def schedule_reminder(self, chat_id, reminder_time, message):
        if isinstance(reminder_time, str):
            reminder = datetime.strptime(reminder_time, '%Y-%m-%d %H:%M:%S.%f')
        else:
            reminder = reminder_time

        if reminder < datetime.now():
            await self.send_reminder(chat_id, message)
        else:
            job = schedule.every().day.at(reminder.strftime('%H:%M')).do(self.send_reminder, chat_id, message)
            self.jobs[job.job_id] = job

    async def cancel_reminder(self, job_id):
        if job_id in self.jobs:
            schedule.cancel_job(self.jobs[job_id])
            del self.jobs[job_id]

    async def run_pending(self):
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)
