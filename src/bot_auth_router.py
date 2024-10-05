

from uuid import uuid4
from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app_auth.auth_models import User, UserTg
from config import config
from const import markups
from sqlalchemy.ext.asyncio import AsyncSession
from markups import auth_user_markup
import re
class AuthState(StatesGroup):
    login_password = State()
    login_success = State()
    register_password = State()
    register_success = State()
    


router = Router()



def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        return True
    else:
        return False

async def check_password(password:str, old_password:bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=old_password)


async def set_autheficated(tg_user_id: int, email: str,  session: AsyncSession) -> None:
   statement = select(User).where(User.email == email).options(selectinload(User.user_tg))
   user = await session.execute(statement)
   user = user.scalar_one_or_none()

   user_tg = UserTg(tg_id=tg_user_id, user_id=user.id, id=uuid4())
   
   session.add(user_tg)
   await session.commit()


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    statement = select(User).where(User.email == email).options(selectinload(User.user_tg))
    user = await session.execute(statement)
    return user.scalar_one_or_none()
   

async def user_is_exists(msg: types.Message, session: AsyncSession) -> None:
    email = msg.text
    statement = select(User).where(User.email == email)
    user = await session.execute(statement)
    user = user.scalar_one_or_none()
    if user is None:
        await msg.answer('Пользователь не найден')
        return False
    else:
        return True

# @router.message(F.text == markups['register'])
# async def register_handler(msg: types.Message, state: FSMContext):
#     await msg.answer(f'Перейдите по ссылке {SITE_URL} для регистрации')
    
    
# @router.message(AuthState.register_password)
# async def register_email_handler(msg: types.Message, state: FSMContext):
#     # СОХРАНЕНИЕ EMAIL
#     email = msg.text
#     await msg.answer('Введите пароль для регистрации')
#     await state.set_state(AuthState.register_success)


# @router.message(AuthState.register_success)
# async def register_password_handler(msg: types.Message, state: FSMContext):
#     # СОХРАНЕНИЕ PASSWORD
#     password = msg.text
#     await msg.answer(f'Вы успешно зарегистрировались в нашей платформе damfai! сайт: {SITE_URL}')
#     await state.clear()   


@router.message(F.text == markups['logout'])
async def logout_handler(msg: types.Message, session: AsyncSession ):
   tg_user_id = msg.from_user.id
   user_tg = await session.scalar(select(UserTg).where(UserTg.tg_id == tg_user_id).options(selectinload(UserTg.user)))
   if user_tg:
           
        await session.delete(user_tg)
        await session.commit()
        await msg.answer(f'Вы успешно вышли из аккаунта damfai! сайт: {config.tg_bot_data.SITE_URL}')
   else:
       await msg.answer('Вы не авторизованы')

   
@router.message(F.text == markups['profile'])
async def profile_handler(msg: types.Message, session: AsyncSession ):
   tg_user_id = msg.from_user.id
   user_tg = await session.scalar(select(UserTg).where(UserTg.tg_id == tg_user_id).options(selectinload(UserTg.user)))


   if user_tg: 
        html_profile = f"""
<b>Профиль пользователя</b>\n
<strong>Имя:</strong> {user_tg.user.name}\n
<strong>Фамилия:</strong> {user_tg.user.surname}\n
<strong>Email:</strong> {user_tg.user.email}
"""
        await msg.answer(html_profile, parse_mode='HTML')
   else:
       await msg.answer('Вы не авторизованы')





email = ''
password = ''
@router.message(F.text == markups['login'])
async def login_handler(msg: types.Message, state: FSMContext):
    await msg.answer('Введите email для входа')
   
    await state.set_state(AuthState.login_password)


@router.message(AuthState.login_password)
async def login_email_handler(msg: types.Message, session: AsyncSession,state: FSMContext):
   if (not (validate_email(msg.text))):
       await msg.answer('Неверный email')
       return
   if not (await user_is_exists(msg, session)):
       return
   email = msg.text
   await msg.answer(f'Ваш email: {email}')
   await state.set_data({'email': msg.text})
   await msg.answer('Введите пароль для входа')
   await state.set_state(AuthState.login_success)
   



@router.message(AuthState.login_success)
async def login_password_handler(msg: types.Message, session: AsyncSession, state: FSMContext):
    if (len(msg.text) < 6):
        await msg.answer('Пароль должен быть не менее 6 символов')
        return
    tg_user_id = msg.from_user.id
    password = msg.text
    data = await state.get_data()
    email = data['email']
    user = await get_user_by_email(email, session)
    if not (await check_password(password, user.password)):
        await msg.answer('Неверный пароль')
        await state.set_state(AuthState.login_password)
        return
    else:
        await set_autheficated(tg_user_id, email, session)
		
    await msg.answer(f'Вы успешно вошли в аккаунт damfai! сайт: {config.tg_bot_data.SITE_URL}', reply_markup=auth_user_markup)
    await state.clear()



 
