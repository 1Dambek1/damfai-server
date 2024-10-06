import datetime
import json
from calendar import monthrange

from fastapi import APIRouter, Depends, HTTPException

from ..books_to_reading.booksRead_models import Reading_Book

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..get_current_me import get_current_user, get_current_id
from ..db import get_session
from ..app_auth.auth_models import User 
from ..books.books_models import Ganre,Book

from .analytics_models import PagesPerDay, MinutesPerDay
from .analytics_schema import CommonReadingInfo, PerDateData, PerMonthData


app = APIRouter(prefix="/analytics", tags=["analytics"])

dates = {
    0:"Monday",
    1:"Tuesday",
    2:"Wednesday",
    3:"Thursday",
    4:"Friday",
    5:"Saturday",
    6:"Sunday"
}

monthes = {
    1:"January",
    2:"February",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",    
    12:"December"
}

# ________________UPDATE ANALYTICS DATA____________________


@app.post("/minutes_per_day/add")
async def add_minutes_per_day(time_minutes:float,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.minutes_per_day)))
    if user:
        minute = await session.scalar(select(MinutesPerDay).where(MinutesPerDay.date == datetime.datetime.now().date(), MinutesPerDay.user_id == user_id))
        if minute:
            minute.minutes_count += time_minutes
        else:
            minute = MinutesPerDay(date=datetime.datetime.now().date(),minutes_count=time_minutes,user_id=user_id)
            session.add(minute)
        await session.commit()
        return True
    

@app.put("/update_sped_words_per_minute")
async def update_sped_words_per_minute(speed:float,me:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    result = eval(me.words_per_minute)
    if speed < 30 or speed > 340:
        raise  HTTPException(status_code=400, detail={"detail":"Speed is too low", "status_code":400})
    if len(result) > 80:
        result = result[30:]
    result.append(speed)
    me.words_per_minute = json.dumps(result)
    await session.commit()
    await session.refresh(me)
    return me.words_per_minute

# ________________GRAPHICS____________________

# reading info
@app.get("/reading_info")
async def get_reading_info(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.reading_books), selectinload(User.minutes_per_day), selectinload(User.pages_per_day)))
    if user:
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
        dataset = {
            "books_count": books_count ,
            "pages_count":pages_count ,
            "words_per_min": (sorted(words_per_minute))[round(len(words_per_minute)/2 - 0.5)],
            "minutes_per_day": minutes_per_day,
            "pages_per_month": pages_per_month,
            "books_per_month": books_per_month,


        }


        return dataset
    
# get pages last 7 days
@app.get("/get_pages_last_7_days", response_model=PerDateData)
async def get_pages_last_7_days(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    last_pages =  await session.scalars(select(PagesPerDay).where(PagesPerDay.user_id == me.id, PagesPerDay.date.between(datetime.datetime.now().date()-datetime.timedelta(days=7), datetime.datetime.now().date())))
    last_pages = last_pages.all()
    dataset = {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,"Sunday":0,
                "end_date":datetime.datetime.now().date(),
                "start_date":datetime.datetime.now().date()-datetime.timedelta(weeks=1)
                }
    for i in last_pages:
        dataset[dates[i.date.weekday()]] = i.pages_count
        
    return dataset

# get minutes last 7 days
@app.get("/get_minutes_last_7_days", response_model=PerDateData)
async def get_pages_last_7_days(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    last_minutes =  await session.scalars(select(MinutesPerDay).where(MinutesPerDay.user_id == me.id, MinutesPerDay.date.between(datetime.datetime.now().date()-datetime.timedelta(days=7), datetime.datetime.now().date())))
    last_minutes = last_minutes.all()
    dataset = {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,"Sunday":0,
                "end_date":datetime.datetime.now().date(),
                "start_date":datetime.datetime.now().date()-datetime.timedelta(weeks=1)
                }
    for i in last_minutes:
        dataset[dates[i.date.weekday()]] = i.minutes_count
        
    return dataset

# get books last 12 months
@app.get("/get_books_last_12_months", response_model=PerMonthData)
async def get_books_last_12_months(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    last_books =  await session.scalars(select(Reading_Book).where(Reading_Book.finish_to_read.between(datetime.datetime.now().date()-datetime.timedelta(days=365), datetime.datetime.now().date())))
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


@app.get("/favourite_ganres")
async def favourite_ganres(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    ganres = await session.scalars(select(Ganre))
    ganres_data = {}
    for i in ganres:
        ganres_data[i.ganre] = 0

    user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.favourite_books).selectinload(Book.ganres), selectinload(User.reading_books).selectinload(Book.ganres)))
    for i in user.favourite_books:
        for i2 in i.ganres:
            ganres_data[i2.ganre] += 1

    for i in user.reading_books:
        for i2 in i.ganres:
            ganres_data[i2.ganre] += 0.5
    
    sorted_data =  {k: v for k, v in sorted(ganres_data.items(), key=lambda item: item[1])}
    # return max(ganres_data, key=ganres_data.get)    
    return sorted_data