from datetime import datetime, timedelta
import re

from ..services import create_new_task_service, delete_task_service, update_task_service
from ...ui import back_to_menu
from ...schemas import TaskCreate, TaskUpdate
from ..classes import AIResponseParser

class AIResponseHandler:
    def __init__(self, raw_content, user_id, db_session):
        self.raw_content = raw_content
        self.user_id = user_id
        self.db = db_session
        self.parser = AIResponseParser(raw_content)
        self.parsed_data = self.parser.parse()
        self.emoji = self.parser.get_emoji()
    
    def _calculate_reminder_time(self, reminder, start_time):
        try:
            reminder_time = datetime.strptime(reminder, '%H:%M').time()
            reminder_datetime = datetime.combine(start_time.date(), reminder_time)

            if reminder_datetime > start_time:
                reminder_datetime -= timedelta(days=1)

            return reminder_datetime
        except ValueError:
            reminder_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(minutes?|hours?)')
            reminder_match = reminder_pattern.match(reminder)

            if reminder_match:
                value = float(reminder_match.group(1))
                unit = reminder_match.group(2)

                if 'hour' in unit:
                    return start_time - timedelta(hours=value)
                else:
                    return start_time - timedelta(minutes=value)
            else:
                return start_time - timedelta(minutes=30)

    async def handle_response(self, message):
        task_data = self.parser.get_event_data(user_id=self.user_id)
        
        if not task_data:
            await message.answer("Не удалось обработать ответ от ИИ.")
            return

        code = task_data.get('code')
        print(task_data)
        match code:
            case "1": 
                await self._create_task(task_data, message)
            case "2":
                await self._update_task(task_data, message)
            case "3":
                await self._search_events(task_data, message)
            case "4": 
                await self._delete_task(task_data, message)
            case "5":
                await message.answer(text=f"{task_data['error']}\n\nПопробуй ещё раз 🔄", reply_markup=back_to_menu())
            case _:
                await message.answer("Что-то пошло не так, попробуй позже ⌛️")

    async def _create_task(self, task_data, message):
        due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d')
        start_time = datetime.combine(due_date, datetime.strptime(task_data['start_time'], '%H:%M').time())
        end_time = datetime.combine(due_date, datetime.strptime(task_data['end_time'], '%H:%M').time())
        reminder_time = self._calculate_reminder_time(task_data['reminder'], start_time)

        new_task = TaskCreate(
            user_id=self.user_id,
            title=task_data['title'],
            description=task_data['description'],
            due_date=due_date,
            start_time=start_time,
            end_time=end_time,
            reminder_time=reminder_time
        )
        emoji = self.emoji if self.emoji else "🎯"
        text_to_user = (
                        f"{emoji} Задача успешно добавлена!\n\nНазвание: {task_data['title']}\n"
                        f"Описание: {task_data['description']}\nВремя начала: {task_data['start_time']}\n"
                        f"Время окончания: {task_data['end_time']}\n"
                        f"Напоминание в {task_data['reminder']}\n"
        )
        if task_data['overlap_warning'] == 'True':
                text_to_user += "⚠️ Внимание: эта задача пересекается с другими задачами!\n"

        await create_new_task_service(body=new_task, db=self.db)
        await message.answer(text=text_to_user, reply_markup=back_to_menu())

    async def _delete_task(self, task_data, message): 
        
        text_to_user =  (
                        f"🗑 Задача успешно удалена!\n\nНазвание: {task_data['title']}\n"
                        f"Описание: {task_data['description']}\nВремя: {task_data['start_time']} {task_data['due_date']} \n"
        )

        await delete_task_service(task_id=task_data['UUID'], db=self.db)
        await message.answer(text=text_to_user, reply_markup=back_to_menu())

    async def _search_events(self, task_data, message):
        events = task_data.get('events', [])
        
        text_to_user = "📋 Ваши задачи:\n\n"
        
        for event in events:
            text_to_user += (
                f"{event['emoji']}\n"
                f"Название: {event['title']} {event['emoji']}\n"
                f"Описание: {event['description']}\n"
                f"Дата: {event['due_date']}\n"
                f"Начало: {event['start_time']}\n"
                f"Окончание: {event['end_time']}\n"
                f"Напоминание в {event['reminder']}\n"
            )
            if event.get('overlap_warning') == 'True':
                text_to_user += "⚠️ Внимание: эта задача пересекается с другими задачами!\n"
            text_to_user += "\n"
        
        if not events:
            text_to_user = "Похоже твоих задач нет 🙁"
        
        await message.answer(text=text_to_user, reply_markup=back_to_menu())

    async def _update_task(self, task_data, message):
        due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d')
        start_time = datetime.combine(due_date, datetime.strptime(task_data['start_time'], '%H:%M').time())
        end_time = datetime.combine(due_date, datetime.strptime(task_data['end_time'], '%H:%M').time())
        reminder_time = self._calculate_reminder_time(task_data['reminder'], start_time)

        new_task = TaskUpdate(
            user_id=self.user_id,
            title=task_data['title'],
            description=task_data['description'],
            due_date=due_date,
            start_time=start_time,
            end_time=end_time,
            reminder_time=reminder_time
        )
        emoji = self.emoji if self.emoji else "🎯"
        text_to_user = (
                        f"{emoji} Задача успешно изменена!\n\nНазвание: {task_data['title']}\n"
                        f"Описание: {task_data['description']}\nВремя начала: {task_data['start_time']}\n"
                        f"Время окончания: {task_data['end_time']}\n"
                        f"Напоминание: {task_data['reminder']}\n"
        )
        if task_data['overlap_warning'] == 'True':
                text_to_user += "⚠️ Внимание: эта задача пересекается с другими задачами!\n"

        await update_task_service(task_id=task_data['UUID'], body=new_task, db=self.db)
        await message.answer(text=text_to_user, reply_markup=back_to_menu())
