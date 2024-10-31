
import datetime
from fastapi import Depends


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..analytics.analytics_models import  MinutesPerDay

from ..db import get_session
from ..app_auth.auth_models import User 
from ..running.running_utils import get_active_running
from ..books.books_models import Book

async def add_minutes_and_points_for_run_per_day(time_minutes:float,book_id:int,me:User,session:AsyncSession ):
    user = await session.scalar(select(User).where(User.id == me.id).options(selectinload(User.minutes_per_day)))
    if user and time_minutes < 60 and time_minutes > 1:
        minute = await session.scalar(select(MinutesPerDay).where(MinutesPerDay.date == datetime.datetime.now().date(), MinutesPerDay.user_id == me.id))
        if minute:
            minute.minutes_count += time_minutes
        else:
            minute = MinutesPerDay(date=datetime.datetime.now().date(),minutes_count=time_minutes,user_id=me.id)
            session.add(minute)
        running = await get_active_running(session)    
        
        if running:
            book = await session.scalar(select(Book).where(Book.id == book_id,Book.author == running.author_name))
            if book:
                user.running_points += 100
        return True
    
