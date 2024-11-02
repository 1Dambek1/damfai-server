from sqlalchemy import select
from markups import auth_user_markup, user_markup
from server.src.app_auth.auth_models import UserTg
from sqlalchemy.ext.asyncio import AsyncSession

async def get_markup(tg_id: int, session: AsyncSession):
    statement = select(UserTg).where(UserTg.tg_id == tg_id)
    user_tg = await session.execute(statement)
    user_tg = user_tg.scalar()

    markup = None
    if user_tg is None:
        markup = user_markup
    else:
        markup = auth_user_markup
    return markup      
	