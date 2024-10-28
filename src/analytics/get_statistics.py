import joblib
from pathlib import Path
import numpy as np

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from calendar import monthrange
import datetime

from sqlalchemy.orm import selectinload
from sqlalchemy import func, select

from .date import dates,monthes

from ..app_auth.auth_models import User
from ..analytics.analytics_models import PagesPerDay, MinutesPerDay
from ..reading_books.booksRead_models import Reading_Book
from ..books.books_models import Ganre,Book

# get_pages_last_7_days
async def get_pages_last_7_days_func(me:User, session:AsyncSession) -> dict:
    last_pages =  await session.scalars(select(PagesPerDay).where(PagesPerDay.user_id == me.id, PagesPerDay.date.between(datetime.datetime.now().date()-datetime.timedelta(days=7), datetime.datetime.now().date())))
    last_pages = last_pages.all()
    dataset = {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,"Sunday":0,
                "end_date":datetime.datetime.now().date(),
                "start_date":datetime.datetime.now().date()-datetime.timedelta(weeks=1)
                }
    for i in last_pages:
        dataset[dates[i.date.weekday()]] = i.pages_count
    return dataset

# get_minutes_last_7_days
async def get_minutes_last_7_days_func(me:User, session:AsyncSession) -> dict:
    last_minutes =  await session.scalars(select(MinutesPerDay).where(MinutesPerDay.user_id == me.id, MinutesPerDay.date.between(datetime.datetime.now().date()-datetime.timedelta(days=7), datetime.datetime.now().date())))
    last_minutes = last_minutes.all()
    dataset = {"Monday":0,
               "Tuesday":0,
               "Wednesday":0,
               "Thursday":0,
               "Friday":0,
               "Saturday":0,
               "Sunday":0,
               "end_date":datetime.datetime.now().date(),
               "start_date":datetime.datetime.now().date()-datetime.timedelta(weeks=1)
                }
    
    for i in last_minutes:
        dataset[dates[i.date.weekday()]] = i.minutes_count
        
    return dataset

# get predict minutes
async def get_predicted_minutes_func(me:User, session:AsyncSession) -> dict:
    BASE_DIR  = Path(__file__).parent.parent.parent
    data = await get_minutes_last_7_days_func(me, session)
    minutes = [data["Wednesday"],data["Thursday"],data["Friday"],data["Saturday"],data["Sunday"]]
    model = joblib.load(BASE_DIR / "ai_models" / "minutes" / "model_random_minutes.pkl")
    
    minutes = (np.array(minutes)).reshape(1, -1)
    predicted_minutes = model.predict(minutes)
    return predicted_minutes[0]

# get predict pages
async def get_predicted_pages_func(me:User, session:AsyncSession) -> dict:
    BASE_DIR  = Path(__file__).parent.parent.parent
    
    data = await get_pages_last_7_days_func(me, session)
    pages = [data["Wednesday"],data["Thursday"],data["Friday"],data["Saturday"],data["Sunday"]]
    
    model = joblib.load(BASE_DIR / "ai_models" / "pages" / "model_random_pages.pkl")
    pages = (np.array(pages)).reshape(1, -1)
    
    predicted_pages = model.predict(pages)
    return predicted_pages[0]

# get common_stats     
async def get_common_statistics_func(user: User, session: AsyncSession) -> dict:
    if user:
        user_id = user.id
        
        books_count = await session.scalar(select(func.count(Reading_Book.book_id)).where(Reading_Book.is_read == True))
        pages_count = 0
        
        for i in user.pages_per_day:
            pages_count += i.pages_count
        minutes_per_day = await session.scalar(select(func.avg(MinutesPerDay.minutes_count)).where(MinutesPerDay.user_id == user_id))
        year = datetime.datetime.now().date().year
        month = datetime.datetime.now().date().month
        start = datetime.date(year, month, 1)
        end = datetime.date(year, month, monthrange(year, month)[1])
        pages_per_month = await session.scalar(select(func.sum(PagesPerDay.pages_count)).where(PagesPerDay.date.between(start, end)))
        books_per_month = await session.scalar(select(func.sum(Reading_Book.book_id)).where(Reading_Book.finish_to_read.between(start, end), Reading_Book.is_read == True))
        words_per_minute:list[int] = eval(user.words_per_minute)
        words_per_min = (sorted(words_per_minute))[round(len(words_per_minute)/2 - 0.5)]
        dataset = {
            "books_count": books_count  or 0,
            "pages_count":pages_count  or 0 ,
            "words_per_min":words_per_min  or 0,
            "minutes_per_day": minutes_per_day  or 0,
            "pages_per_month": pages_per_month or 0,
            "books_per_month": books_per_month  or 0,
            "predicted_minutes": await get_predicted_minutes_func(user, session),
            "predicted_pages": await get_predicted_pages_func(user, session),
        }
        return dataset


# get_books_last_12_months
async def get_books_last_12_months_func(me:User, session:AsyncSession) -> dict:
    last_books =  await session.scalars(select(Reading_Book)
                                        .where(Reading_Book.finish_to_read.between(datetime.datetime.now().date()-datetime.timedelta(days=365), datetime.datetime.now().date()),
                                               Reading_Book.user_id == me.id))
    last_books = last_books.all()
    dataset = {
    "January":0,
    "February":0,
    "March":0,
    "April":0,
    "May":0,
    "June":0,
    "July":0,
    "August":0,
    "September":0,
    "October":0,
    "November":0,    
    "December":0
}
    for i in last_books:
        dataset[monthes[i.finish_to_read.month]] += 1
        
    return dataset

# get_favourite_ganres
async def get_favourite_ganres_func(me:User, session:AsyncSession) -> dict:
    ganres = await session.scalars(select(Ganre))
    ganres_data = {i.ganre: 0 for i in ganres}

    user = await session.scalar(select(User)
                                .where(User.id == me.id)
                                .options(selectinload(User.favourite_books)
                                         .selectinload(Book.ganres),
                                         selectinload(User.reading_books)
                                         .selectinload(Book.ganres)))

    for fav_book in user.favourite_books:
        for genre in fav_book.ganres:
            ganres_data[genre.ganre] += 0.98

    for reading_book in user.reading_books:
        for genre in reading_book.ganres:
            ganres_data[genre.ganre] += 0.77
    
    return max(ganres_data, key=ganres_data.get)   
    # sorted_data =  {k: v for k, v in sorted(ganres_data.items(), key=lambda item: item[1])} 
    return ganres_data

