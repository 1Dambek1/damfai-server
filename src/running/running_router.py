
import asyncio
import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from .running_models import Running, Status, Winner, Prize
from .running_utils import get_active_running
from .running_schema import RunningSchema, WinnerSchema, PrizeSchema,RankingSchema

from ..get_current_me import  get_current_user
from ..app_auth.auth_models import User
from ..db import get_session, session
from ..books.books_models import Book, Chapter, PageModel, Authors, Rating
from ..analytics.analytics_models import PagesPerDay

from ..utils.common_schema import ShowBook

from ..scheduler_connect import cancel_running_task
app = APIRouter(prefix="/running", tags=["running"])


# get active running with prizes
@app.get("/acitve_running", response_model=RunningSchema)
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
    raise HTTPException(detail={"detail":"This running is not exist", "status_code":400}, status_code=400)

# places of active running
@app.get("/place")
async def get_running_places(me:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):

    ranked_users = (
        select(
            User.id,
            User.name,
            User.surname,
            User.running_points,
            func.row_number().over(order_by=User.running_points.desc()).label("ranking")
        )
        .order_by(User.running_points.desc())
        .limit(100)
    )
    
    your_rank = (
        select(
            User.id,
            User.name,
            User.surname,
            User.running_points,
            func.row_number().over(order_by=User.running_points.desc()).label("ranking")
        )
        .order_by(User.running_points.desc())
        .where(User.id == me.id)
    )
    
    # Выполняем запросы
    your_rank = await session.execute(your_rank)
    
    rank_row = your_rank.fetchone()

    user_rank_dict = {
            "id": rank_row[0],
            "name": rank_row[1],
            "surname": rank_row[2],
            "running_points": rank_row[3],
            "rank": rank_row[4]
        }
    
    result = await session.execute(ranked_users)
    
    
    # Преобразуем результат в словарь
    top_100_users_dict = {
        "top_100_users": [
        {
            "id": user_id,
            "name": name,
            "surname": surname,
            "running_points": running_points,
            "rank": ranking
        }
        for user_id, name, surname, running_points, ranking in result
    ],
        "your_rank": user_rank_dict
        }
    
    return top_100_users_dict
    
# get books by running
@app.get("/books", response_model=list[ShowBook])
async def get_books(session:AsyncSession = Depends(get_session)):
    running = await get_active_running(session)
    if running:
        query = (
            select(
                Book,
                func.count(Chapter.id).label("chapters"),
                func.coalesce(func.avg(Rating.rating), 0).label("average_rating")
            )
            .join(Book.chapters, isouter=True)  
            .join(Book.ratings,  isouter=True)
            .options(selectinload(Book.ganres))    
            .group_by(Book.id)
            .order_by(func.random())
            .where(Book.author == running.author_name)
        )
        result = await session.execute(query)
        dataset = []
        for row in result.all():
            book = row[0]  
            average_rating = row.average_rating  
            chapters = row.chapters  

            book_dict = book.__dict__
            book_dict["ganres"] = [ganre.ganre for ganre in book_dict["ganres"]]  
            book_dict["ratings"] = average_rating  
            book_dict["chapters"] = chapters  

            dataset.append(book_dict)  

        
        return dataset
    raise HTTPException(detail={"detail":"This running is not exist", "status_code":400}, status_code=400)
    
    
# ________test________________
@app.get("/authors")
async def get_authors(session:AsyncSession = Depends(get_session)):
    authors = await session.scalars(select(Authors).options(selectinload(Authors.books)))
    return authors.all()

