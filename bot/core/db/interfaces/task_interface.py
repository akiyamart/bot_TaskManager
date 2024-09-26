from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import Union

from ..models import Task, TaskStatus

class TaskDAL:
    def __init__(self, db_connect: AsyncSession):
        self.db_connect = db_connect

    async def create_task(
            self, user_id: int, title: str, description: str = None, due_date: datetime = None, end_time: datetime = None
        ) -> Task:
        new_task = Task(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            end_time=end_time
        )
        self.db_connect.add(new_task)
        await self.db_connect.flush()
        return new_task
        
    async def get_user_tasks(
            self, user_id: int
        ) -> list[Task]:
        stmt = select(Task).where(Task.user_id == user_id)
        result = await self.db_connect.execute(stmt)
        return result.scalars().all()

    async def delete_task(self, task_id: int) -> None:
        stmt = select(Task).where(Task.id == task_id)
        result = await self.db_connect.execute(stmt)
        task = result.scalars().first()
        if task:
            await self.db_connect.delete(task)

    async def update_task(
            self, task_id: int, title: str, description: str, due_date: datetime, end_time: datetime
        ) -> Task:
        stmt = select(Task).where(Task.id == task_id)
        result = await self.db_connect.execute(stmt)
        task = result.scalars().first()

        if task:
            task.title = title
            task.description = description
            task.due_date = due_date
            task.end_time = end_time
            await self.db_connect.flush()

        return task