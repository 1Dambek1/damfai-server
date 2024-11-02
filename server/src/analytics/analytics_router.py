
import json

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from server.src.db import get_session
from server.src.get_current_me import get_current_user
from server.src.app_auth.auth_models import User 

from .analytics_schema import PerDateData, PerMonthData, CommonReadingInfo
from .get_statistics import (
get_common_statistics_func,
get_pages_last_7_days_func,
get_minutes_last_7_days_func,
get_books_last_12_months_func,
get_favourite_ganres_func,
)

app = APIRouter(prefix="/analytics", tags=["analytics"])

# ________________UPDATE ANALYTICS DATA____________________

# update speed words per minute
@app.put("/update_speed_words_per_minute")
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

# reading common info
@app.get("/reading_info", response_model=CommonReadingInfo)
async def get_reading_info(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.id == me.id).options(selectinload(User.reading_books), selectinload(User.minutes_per_day), selectinload(User.pages_per_day)))
    return await get_common_statistics_func(user, session)

# get count pages last 7 days
@app.get("/get_pages_last_7_days", response_model=PerDateData)
async def get_pages_last_7_days(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):  
    return await get_pages_last_7_days_func(me, session)

# get minutes last 7 days
@app.get("/get_minutes_last_7_days", response_model=PerDateData)
async def get_minutes_last_7_days(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    return await get_minutes_last_7_days_func(me, session)

# get books last 12 months
@app.get("/get_books_last_12_months", response_model=PerMonthData)
async def get_books_last_12_months(me:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    return await get_books_last_12_months_func(me, session)

@app.get("/favourite_ganres")
async def favourite_ganres(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    return await get_favourite_ganres_func(me, session)

