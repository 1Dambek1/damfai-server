import logging
import sys
# Imports WORKING!
sys.path.append('/app')

# for working relations
from bot.src.utils.get_markup import get_markup

from server.src.bookmarks.bookmarsk_models import FavouriteUser, BookmarkUser
from server.src.themes.themes_models import Theme
from server.src.books.books_models import Book, PageModel
from server.src.analytics.analytics_models import PagesPerDay, MinutesPerDay
from server.src.reading_books.booksRead_models import Reading_Book
from server.src.extensions.extensions_models import Extension, ExtensionUser
from server.src.themes.themes_models import Theme, ThemeUser
from server.src.app_auth.auth_models import User, UserTg


from sqlalchemy import select
import asyncio
from middleware.db import SessionMiddleware
from auth.router import router as auth_router
from books.router import router as books_router
from analytics.router import router as analytics_router
from summarize.router import router as summarize_router
from aiogram import Bot, Dispatcher, Router
from server.src.running.running_utils import get_active_running
from server.src.db import session
from aiogram.filters import Command
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from config import config
from aiogram import Bot, Dispatcher
from aiogram3_triggers import TRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from server.src.db import session
from apscheduler.util import utc
from sqlalchemy.orm import selectinload
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


user_data = {}
scheduler_state = {"started": False}
bot = Bot(config.env.BOT_TOKEN)
dp = Dispatcher()  

dp.update.middleware(SessionMiddleware(session_pool=session))
router = Router(name="main")
@router.message(Command('start'))
async def start(msg: types.Message, session: AsyncSession):
    text = rf'Приветствуем в damfai, {msg.from_user.mention_html()}!'
    tg_id = msg.from_user.id

    markup = await get_markup(tg_id, session)
    user_data['chat_id'] = msg.chat.id
    if not scheduler_state['started']:
        await start_scheduler(msg, bot, tg_id, session)

    
    await msg.answer(text=text, reply_markup=markup, parse_mode='HTML')



notify_router = TRouter()

scheduler = AsyncIOScheduler()
scheduler.configure(timezone=utc)
async def find_book_to_read(session: AsyncSession):
    book = await session.scalar(select(Reading_Book).where(not Reading_Book.is_read).order_by(Reading_Book.target_of_date).limit(1).options(selectinload(Reading_Book.book)))
    return book

# Функция для отправки уведомления пользователю
async def send_reminder_to_user(chat_id: int, bot: Bot, session: AsyncSession):
    book = await find_book_to_read(session)
    message = None
    if book:
        message = f"Не забудь прочитать сегодня: {book.book.title}"
    else:
        message = f"Хей, давно хотел начать читать? Заходи на сайт {config.env.SITE_URL}/books и выбирай подходящую книгу для прочтения!"
    await bot.send_message(chat_id=chat_id, text=message)

# Триггер, который будет срабатывать каждый день
@notify_router.triggers_handler('day')
async def notify_to_read_book_every_day(dp: Dispatcher, bot: Bot):
    async with session() as connection:
        if 'chat_id' in user_data and user_data['chat_id']:
            await send_reminder_to_user(user_data["chat_id"], bot, connection)


async def notify_user_about_running(chat_id: int, bot: Bot, session: AsyncSession):
    running = await get_active_running(session)
    message = None
    if running:
        message = f"Гонка еще идёт! Не забудь почитать книги автора {running.author_name}. Конец гонки {running.end_running_date}"
        
    else:
        message = f"Гонка завершена! перейди по ссылке чтобы увидеть результаты: {config.env.SITE_URL}/race"

        
    await bot.send_message(chat_id=chat_id, text=message)


@notify_router.triggers_handler('day')
async def notify_user_to_go_read_books_in_running(dp: Dispatcher, bot: Bot):
    async with session() as connection:
        if 'chat_id' in user_data and user_data['chat_id']:
            await notify_user_about_running(user_data["chat_id"], bot, connection)

# Запуск планировщика
async def start_scheduler(dp: Dispatcher, bot: Bot, tg_id: int, session: AsyncSession):
    scheduler.add_job(
        send_reminder_to_user,
        trigger='cron',
        hour=12,
        minute=0,
        kwargs={"chat_id": dp.chat.id, "bot": bot, "session": session }
    )
    
    scheduler.add_job(
        notify_user_about_running,
        trigger='cron',
        hour=12,
        minute=0,
        kwargs={"chat_id": dp.chat.id, "bot": bot, "session": session }
    )
    scheduler_state['started'] = True
    scheduler.start()
    
    




async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    dp.include_router(router)
    dp.include_router(auth_router)
    dp.include_router(notify_router)
    dp.include_router(books_router)
    dp.include_router(analytics_router)
    dp.include_router(summarize_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
