
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from fastapi import APIRouter, Depends
from fastapi_pagination import  add_pagination,Page,paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from fastapi_filter import FilterDepends

from server.src.bookmarks.bookmarsk_models import FavouriteUser
from server.src.books.books_models import Ganre, Chapter
from server.src.get_current_me import get_current_id, get_current_user
from server.src.app_auth.auth_models import User
from server.src.db import get_session
from server.src.books.books_models import Book,Rating, Authors
from server.src.utils.common_schema import ShowBook

from .search_system_utils import find_most_similar
from .books_filter import BookFilter

disable_installed_extensions_check()


app = APIRouter(prefix="/recommendations", tags=["recommendations"])

# # search book per ganre(redact)
@app.get("/books/per_ganre")
async def per_ganre(session:AsyncSession = Depends(get_session)):
    ganres = (await session.scalars(select(Ganre).options(selectinload(Ganre.books)).order_by(func.random()).limit(5))).all()
    books = []
    for ganre in ganres:
            books.append({f"{ganre.ganre}":ganre.books})
    return books

# search book per author(redact)
@app.get("/books/per_author")
async def per_author(session:AsyncSession = Depends(get_session)):
    authors = (await session.scalars(select(Authors).options(selectinload(Authors.books)).order_by(func.random()).limit(3))).all()
    books = []
    for author in authors:
            books.append({f"{author.author}":author.books})
    return books

# search book(redact)
@app.get("/books/get_reccomendations")
async def get_reccomendations(session:AsyncSession = Depends(get_session), user_id:int = Depends(get_current_id), current_user:User = Depends(get_current_user)):
        select_books = await session.scalars(select(FavouriteUser).where(FavouriteUser.user_id==user_id).options(selectinload(FavouriteUser.book)).order_by(func.random()).limit(10))
        select_books = select_books.all()
        
        rate_books = await session.scalars(select(Rating).where(Rating.user_id==user_id, Rating.rating>=4).options(selectinload(Rating.book)).order_by(func.random()).limit(10))
        rate_books = rate_books.all()
        
        texts_select = [book.book.zip_text for book in select_books]
        texts_rate = [book.book.zip_text for book in rate_books]
        texts = list(set(texts_select + texts_rate))
        
        canditate_books = await session.scalars(select(Book)
                                                .where(Book
                                                       .id
                                                       .not_in
                                                       ([s_book.book_id for s_book in select_books]+[r_book.book_id for r_book in rate_books]))
                                                .options(selectinload(Book.ganres), selectinload(Book.ratings))
                                                .order_by(func.random()))
        
        return find_most_similar(texts=texts,
                                candidate_texts=canditate_books.all())


# search book(redact)
@app.post("/books/search")
async def search(
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
