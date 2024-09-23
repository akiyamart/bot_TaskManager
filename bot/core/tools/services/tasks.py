from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from ...schemas import TaskCreate, ShowTaskResponse  
from ...db.interfaces import TaskDAL

async def create_new_task(body: TaskCreate, db: AsyncSession) -> Union[ShowTaskResponse, None]:
    async with db.begin():
        task_dal = TaskDAL(db)

        new_task = await task_dal.create_task(
            user_id=body.user_id,
            title=body.title,
            description=body.description,
            status=body.status,
            due_date=body.due_date 
        )

        return ShowTaskResponse(
            id=new_task.id,
            user_id=new_task.user_id,
            title=new_task.title,
            description=new_task.description,
            status=new_task.status.value,
            created_at=new_task.created_at,
            due_date=new_task.due_date
        )
