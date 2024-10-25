
import datetime
import logging

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..bookmarks.bookmarsk_models import FavouriteUser
from ..books.books_models import Ganre
from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book,Rating

from .recomendations_utils import find_most_similar
from .recomendations_schema import ShowRecomendations


app = APIRouter(prefix="/recomendations", tags=["recomendations"])

@app.get("/books_per_ganre")
async def you_should_continue(session:AsyncSession = Depends(get_session)):
    ganres = (await session.scalars(select(Ganre).options(selectinload(Ganre.books)).order_by(func.random()).limit(5))).all()
    books = []
    for i in ganres:
            books.append({f"{i.ganre}":i.books})
    return books
                

@app.get("/get_reccomendation_books")
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



