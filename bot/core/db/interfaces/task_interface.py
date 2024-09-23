from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from datetime import datetime
from typing import Union, Dict

from ..models import Task, TaskStatus


class TaskDAL:
    def __init__(self, db_connect: AsyncSession):
        self.db_connect = db_connect

    async def create_task(
            self, user_id: int, title: str, description: str = None, status: TaskStatus = TaskStatus.pending, due_date: datetime = None
        ) -> Task:
        new_task = Task(
            user_id=user_id,
            title=title,
            description=description,
            status=status,
            due_date=due_date
        )
        self.db_connect.add(new_task)
        await self.db_connect.flush()
        return new_task
    