from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Dict

from ...schemas import UserCreate, ShowUserResponse
from ...db.interfaces import UserDAL

async def create_new_user(body: UserCreate, user_dal: UserDAL) -> Union[ShowUserResponse, None]:
    new_user = await user_dal.create_user(
        id = body.id
    )

    return ShowUserResponse(
        id = new_user.id
    )
    
async def get_user(body: UserCreate, db: AsyncSession) -> Union[ShowUserResponse, None]:
    async with db.begin(): 
        user_dal = UserDAL(db)

        user = await user_dal.get_user(
            id=body.id
        )

        if not user:
            user = await create_new_user(
                UserCreate(id=body.id), 
                user_dal=user_dal
            )

        return ShowUserResponse(
            id = user.id
        )