
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from .running_models import Running
from .running_utils import get_active_running
from .running_schema import RunningSchema,RankingSchema

from server.src.get_current_me import  get_current_user
from server.src.app_auth.auth_models import User
from server.src.db import get_session
from server.src.books.books_models import Book, Chapter, Rating

from server.src.utils.common_schema import ShowBook

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
async def get_running_id(id_running:int, me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    running = await session.scalar(select(Running).options(selectinload(Running.prizes), selectinload(Running.winners)).where(Running.id == id_running))
    if running:
        return running
    raise HTTPException(detail={"detail":"This running is not exist", "status_code":400}, status_code=400)

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
    

