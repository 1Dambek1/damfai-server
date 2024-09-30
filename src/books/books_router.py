from typing import Optional

import pandas as pd

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.logger import logger

from fastapi_pagination import  add_pagination,Page,paginate
from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()

from fastapi_filter import FilterDepends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload, aliased
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError

from ..get_current_me import get_current_user
from ..db import get_session

from .books_schema import CreateBook, CreateRating, ShowBook, ShowChapter, CreateChapter, CreatePage, ShowPage, ShowGanres
from .books_models import Book, Chapter, PageModel, Rating, Ganre,GanreBook
from .books_filter import BookFilter
app = APIRouter(prefix="/books", tags=["books"])

@app.get("")
async def bo(session:AsyncSession = Depends(get_session)):
    books = await session.scalars(select(Book).options(selectinload(Book.chapters), selectinload(Book.ratings), selectinload(Book.ganres)))
    return books.all()

@app.post("")
async def get_books(ganres:list[int] = None,me = Depends(get_current_user),user_filter: Optional[BookFilter] = FilterDepends(BookFilter),session:AsyncSession = Depends(get_session)) -> Page[ShowBook]:
    query1 = user_filter.filter(select(Book).options(selectinload(Book.chapters), selectinload(Book.ratings), selectinload(Book.ganres)))
    result = await session.execute(query1)
    result = result.scalars().all()
    datas = []

    for i in result:
        new_ganres = [i.ganre for i in i.ganres]

        if ganres in new_ganres:   
            data = {
                "id":i.id,
                "title":i.title,
                "file_path":i.file_path,
                "author":i.author,
                "desc":i.desc,
                "writen_date":i.writen_date,
                "chapters":len(i.chapters),
                "ganres":new_ganres
                }
            counts = 0 
            if len(i.ratings)>0:
                for i2 in i.ratings: 
                    counts += i2.rating
            
                data["ratings"] = counts/len(i.ratings)
            else:
                data["ratings"] = 0
            datas.append(data)
        
    return paginate(datas)




@app.get("/chapters/{id_book}", response_model=list[ShowChapter])
async def get_books_with_chapters(id_book:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    query1 = (select(Chapter).options(joinedload(Chapter.pages)).where(Chapter.book_id == id_book))
    result = await session.execute(query1)
    result = result.scalars().all()
    datas = []
    for i in result:
            data = {
                "id":i.id,
                "title":i.title,
                "numberOfChapter":i.numberOfChapter,
                "pages":len(i.pages),
            }

            datas.append(data)
    return datas


@app.get("/get_pages_by_chapter/{id_chapter}")
async def get_pages_by_chapter(id_chapter:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)) -> Page[ShowPage] :
    query1 = (select(PageModel).where(PageModel.chapter_id == id_chapter))
    result = await session.execute(query1)
    return paginate(result.scalars().all())





#  Rating

@app.post("/book/rating")
async def create_rating(rating:CreateRating,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    try:
        rating = Rating(book_id = rating.book_id, rating=rating.rating, user_id=me.id)
        session.add(rating)
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail={
                "data":"book is not exist",
                "status":400
        })
    await session.refresh(rating)
    return rating







@app.get("/ganres/all", response_model = list[ShowGanres])
async def ganres(me = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    ganres = await session.scalars(select(Ganre))
    return ganres.all()






@app.post("/ganres/create")
async def create_ganre(ganre:str,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    ganre_m = Ganre(ganre=ganre)
    session.add(ganre_m)
    await session.commit()
    await session.refresh(ganre_m) 
    return ganre_m

@app.post("/create")
async def create_book(book:CreateBook,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    
    book = Book(title = book.title, author = book.author, desc = book.desc, writen_date = book.writen_date)
    for i in book.ganres:
        ganre = await session.scalar(select(Ganre).where(Ganre.id == i))
        if ganre:
            book.ganres.append(ganre)
        
    session.add(book)
    

            # await session.flush()
    await session.commit()
    await session.refresh(book)
    return book


add_pagination(app)  



# @app.get("/students") 
# async def get_students(me = Depends(get_current_active_user),user_filter: Optional[StudentFilter] = FilterDepends(StudentFilter),session:AsyncSession = Depends(get_session)) -> Page[ShowUser]:
#     query = user_filter.filter(select(User).where(User.role == Role.student))   # 
#     result = await session.execute(query)
#     return paginate(result.scalars().all())




# @app.get("/booksp")
# async def get_books_paginate(me = Depends(get_current_user),session:AsyncSession = Depends(get_session))-> Page[ShowBook]:
#     result = await session.execute(select(Book).options(Book.chapters))

#     return paginate(result.scalars().all())



# @app.get("/booksf")
# async def get_books_filter(me = Depends(get_current_user),
#                     user_filter: Optional[BookFilter] = FilterDepends(BookFilter),
#                     session:AsyncSession = Depends(get_session)):
    
#     query = user_filter.filter(select(Book).options(Book.chapters)) 
#     result = await session.execute(query)

#     return result.scalars().all()



# @app.get("/bookss")
# async def g(me = Depends(get_current_user),
#                     session:AsyncSession = Depends(get_session)):
    
#     result = await session.execute(select(Book).options(Book.chapters))

#     return result.scalars().all()
