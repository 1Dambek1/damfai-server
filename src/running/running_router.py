
import asyncio
import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from .running_models import Running, Status, Winner, Prize
from .running_utils import get_active_running
from .running_schema import RunningSchema, WinnerSchema, RankingSchema

from ..get_current_me import  get_current_user
from ..app_auth.auth_models import User
from ..db import get_session, session
from ..books.books_models import Book, Chapter, PageModel, Authors
from ..analytics.analytics_models import PagesPerDay

from ..scheduler_connect import cancel_running_task
app = APIRouter(prefix="/running", tags=["running"])


# get active running with prizes
@app.get("/active", response_model=RunningSchema)
async def get_running(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    running = await get_active_running(session=session)
    if running:
        return running
    raise HTTPException(detail={"detail":"You are have not running", "status_code":400}, status_code=400)

# get running by id
@app.get("/running/{id_running}", response_model=RunningSchema)
async def get_running(id_running:int, me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    running = await session.scalar(select(Running).options(selectinload(Running.prizes), selectinload(Running.winners)).where(Running.id == id_running))
    if running:
        return running
    raise HTTPException(detail={"detail":"You are have not running", "status_code":400}, status_code=400)

# places of active running
@app.get("/leaderboard", response_model=RankingSchema)
async def get_running_places(me:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    top_users_query = (
        select(
            User.id,
            User.name,
            User.surname,
            User.running_points,
            func.row_number().over(order_by=User.running_points.desc()).label("place")
        )
        .order_by(User.running_points.desc())
        .limit(100)
    )
    
    user_rank_query = (
        select(
            User.id,
            User.name,
            User.surname,
            User.running_points,
            func.row_number().over(order_by=User.running_points.desc()).label("place")
        )
        .order_by(User.running_points.desc())
        .where(User.id == me.id)
    )

    
    # Выполняем запросы
    user_rank = await session.execute(user_rank_query)
    rank_row = user_rank.fetchone()
    
    result = await session.execute(top_users_query)

    user_rank = {
        "id": rank_row[0],
        "name": rank_row[1],
        "surname": rank_row[2],
        "runningPoints": rank_row[3],
        "place": rank_row[4]
    }
    
    top_users = [
        {
            "id": id,
            "name": name,
            "surname": surname,
            "runningPoints": running_points,
            "place": place
        } for id, name, surname, running_points, place in result
    ]

    # Преобразуем результат в словарь
    leaderboard = {
        "topUsers": top_users,
        "userRank": user_rank
    }
    
    return leaderboard
    
    
# ________test________________
@app.get("/authors")
async def get_authors(session:AsyncSession = Depends(get_session)):
    authors = await session.scalars(select(Authors).options(selectinload(Authors.books)))
    return authors.all()

@app.post("/add_running", description="debug")
async def add_running(author:str,days:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    running = await get_active_running(session=session)
    if running:
        raise HTTPException(detail={"detail":"You are already have running", "status_code":400}, status_code=400)
    
    author = await session.scalar(select(Authors).where(Authors.author == author))
    if author:
        start_running_date =datetime.datetime.now(datetime.timezone.utc)
        start_running_date = start_running_date.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        
        running = Running(status = Status.started, name_running="gool",start_running_date=start_running_date,end_running_date=start_running_date + datetime.timedelta(days=days))
        running.author = author
        running.author_name = author.author

        
        for i in range(10):
            prize = Prize(place = i+1, chappi_tokens = 100*(10-1), running_id = running.id)
            running.prizes.append(prize)
        session.add(running)
        await session.commit()
        asyncio.create_task(cancel_running_task())
        return True
    