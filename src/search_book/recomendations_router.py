
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
from ..books.books_models import Ganre
from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book,Rating

from .recomendations_utils import find_most_similar
from .recomendations_schema import ShowBook
from .books_filter import BookFilter


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


@app.post("")
async def get_books(ganres:list[int],rating__lte:float = None, rating__gte:float = None,user_filter: Optional[BookFilter] = FilterDepends(BookFilter),session:AsyncSession = Depends(get_session))-> Page[ShowBook] :
    query1 = user_filter.filter(select(Book).options(selectinload(Book.chapters), selectinload(Book.ratings), selectinload(Book.ganres)))
    result = await session.execute(query1)
    result = result.scalars().all()
    datas = []
    for i in result:
            is_good = True  
            mine_ganres = [i2.id for i2 in i.ganres]                     
            for i2 in ganres:
                if i2 not in mine_ganres:
                       is_good = False
            if is_good:
                data = {
                            "id":i.id,
                            "title":i.title,
                            "file_path":i.file_path,
                            "author":i.author,
                            "desc":i.desc,
                            "writen_date":i.writen_date,
                            "chapters":len(i.chapters),
                            "ganres":[i.ganre for i in i.ganres],
                            "age_of_book": i.age_of_book,

                            }
                # rating
                sum_rating = 0 
                if len(i.ratings)>0:
                    for i2 in i.ratings: 
                        sum_rating += i2.rating
                    rate = sum_rating/len(i.ratings)
                    data["ratings"] = rate
                else:
                    rate = 0
                    data["ratings"] = rate

                if rating__lte and rating__gte:
                    if rate >= rating__gte and rate <= rating__lte:
                        datas.append(data)

                elif rating__lte:
                    if rate <= rating__lte:
                        datas.append(data)

                elif rating__gte:
                    if rate >= rating__gte:
                        datas.append(data)
                else:
                    datas.append(data)
        
    return paginate(datas)




add_pagination(app)
