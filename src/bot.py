

import logging
from uuid import uuid4
import bcrypt
from sqlalchemy import select
from config import config
import asyncio
from tg_bot.db import SessionMiddleware
from bot_auth_router import router as auth_router
from aiogram import Bot, Dispatcher, Router
from db import session
from aiogram.filters import Command
from aiogram import types
from markups import auth_user_markup, user_markup
from sqlalchemy.ext.asyncio import AsyncSession
from src.app_auth.auth_models import User, UserTg
bot = Bot(config.tg_bot_data.TOKEN)
dp = Dispatcher()  
dp.update.middleware(SessionMiddleware(session_pool=session))
router = Router(name="main")
@router.message(Command('start'))
async def start(msg: types.Message, session: AsyncSession):
    text = rf'Приветствуем в damfai, {msg.from_user.mention_html()}!'
    tg_id = msg.from_user.id
    start_user = User(
    name="Александр",
    surname="Шаронов",
    email="shmsmms01@gmail.com",
    id=uuid4(),
    password=bcrypt.hashpw(password='12345678'.encode(), salt=bcrypt.gensalt())
)
    session.add(start_user)
    await session.flush()
    statement = select(UserTg).where(UserTg.tg_id == tg_id)
    user_tg = await session.execute(statement)
    user_tg = user_tg.scalar_one_or_none()

    await session.commit()
    markup = None
    if user_tg is None:
        markup = user_markup
    else:
        markup = auth_user_markup
    await msg.answer(text=text, reply_markup=markup, parse_mode='HTML')


async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    dp.include_router(router)
    dp.include_router(auth_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
