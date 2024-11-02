

import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...server.src.app_auth.auth_models import User, UserTg


async def get_current_me(user_tg_id: int, session: AsyncSession) -> User:
    return await session.scalar(select(UserTg).where(UserTg.tg_id == user_tg_id)) # Получение пользователя по user_tg_id


