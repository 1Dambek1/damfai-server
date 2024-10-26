
import datetime
import logging
from typing import Optional

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


from fastapi import APIRouter, Depends

from fastapi_pagination import  add_pagination,Page,paginate
from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()
from fastapi_filter import FilterDepends

from ..bookmarks.bookmarsk_models import FavouriteUser
from ..books.books_models import Ganre, Chapter
from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book,Rating, Authors
from ..utils.common_schema import ShowBook

from .recomendations_utils import find_most_similar
from .books_filter import BookFilter


app = APIRouter(prefix="/recomendations", tags=["recomendations"])

# # search book per ganre(redact)
@app.get("/books/per_ganre")
async def you_should_continue(session:AsyncSession = Depends(get_session)):
    ganres = (await session.scalars(select(Ganre).options(selectinload(Ganre.books)).order_by(func.random()).limit(5))).all()
    books = []
    for i in ganres:
            books.append({f"{i.ganre}":i.books})
    return books

# search book per author(redact)
@app.get("/books/per_author")
async def you_should_continue(session:AsyncSession = Depends(get_session)):
    authors = (await session.scalars(select(Authors).options(selectinload(Authors.books)).order_by(func.random()).limit(3))).all()
    books = []
    for i in authors:
            books.append({f"{i.author}":i.books})
    return books

# search book(redact)
@app.get("/books/get_reccomendations")
async def test2(session:AsyncSession = Depends(get_session), user_id:int = Depends(get_current_id), current_user:User = Depends(get_current_user)):
        select_books = await session.scalars(select(FavouriteUser).where(FavouriteUser.user_id==user_id).options(selectinload(FavouriteUser.book)).order_by(func.random()).limit(10))
        select_books = select_books.all()
        
        rate_books = await session.scalars(select(Rating).where(Rating.user_id==user_id, Rating.rating>=4).options(selectinload(Rating.book)).order_by(func.random()).limit(10))
        rate_books = rate_books.all()
        
        texts_select = [book.book.zip_text for book in select_books]
        texts_rate = [book.book.zip_text for book in rate_books]
        texts = list(set(texts_select + texts_rate))
        
        canditate_books = await session.scalars(select(Book).where(Book.id.not_in([i.book_id for i in select_books]+[i.book_id for i in rate_books])).options(selectinload(Book.ganres), selectinload(Book.ratings)).order_by(func.random()))
        
        return find_most_similar(texts=texts,
                                candidate_texts=canditate_books.all())


# search book(redact)
@app.post("/books/search")
async def get_books(
    session: AsyncSession = Depends(get_session),
    ganres:list[int] = None,
    rating__lte:float = 5,
    rating__gte:float = 0,
    user_filter: Optional[BookFilter] = FilterDepends(BookFilter),
) -> Page[ShowBook] :
    
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
    )
    query = query.having(func.coalesce(func.avg(Rating.rating), 0).between(rating__gte, rating__lte))
    if ganres:
        query = query.join(Book.ganres).filter(Ganre.id.in_(ganres))  
    query = user_filter.filter(query)
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



    return paginate(dataset)



add_pagination(app)
