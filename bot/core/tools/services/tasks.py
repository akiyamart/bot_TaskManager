from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List
from datetime import datetime

from ...schemas import TaskCreate, ShowTaskResponse, TaskUpdate 
from ...db.interfaces import TaskDAL

async def create_new_task_service(body: TaskCreate, db: AsyncSession) -> Union[ShowTaskResponse, None]:
    async with db.begin():
        task_dal = TaskDAL(db)

        new_task = await task_dal.create_task(
            user_id=body.user_id,
            title=body.title,
            description=body.description,
            due_date=body.due_date,
            end_time=body.end_time
        )

        return ShowTaskResponse(
            id=new_task.id,
            user_id=new_task.user_id,
            title=new_task.title,
            description=new_task.description,
            due_date=new_task.due_date,
            end_time=new_task.end_time 
        )

async def get_user_tasks_service(user_id: int, db: AsyncSession) -> List[ShowTaskResponse]:
    async with db.begin():
        task_dal = TaskDAL(db)
        
        tasks = await task_dal.get_user_tasks(user_id)
        
        return [
            ShowTaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                due_date=task.due_date,
                end_time=task.end_time
            ) for task in tasks
        ]

async def delete_task_service(task_id: int, db: AsyncSession) -> None:
    async with db.begin():
        task_dal = TaskDAL(db)
        await task_dal.delete_task(task_id)

async def update_task_service(task_id: int, body: TaskUpdate, db: AsyncSession) -> Union[ShowTaskResponse, None]:
    async with db.begin():
        task_dal = TaskDAL(db)

        updated_task = await task_dal.update_task(
            task_id=task_id,
            title=body.title,
            description=body.description,
            due_date=body.due_date,
            end_time=body.end_time
        )

        return ShowTaskResponse(
            id=updated_task.id,
            user_id=updated_task.user_id,
            title=updated_task.title,
            description=updated_task.description,
            due_date=updated_task.due_date,
            end_time=updated_task.end_time
        )
