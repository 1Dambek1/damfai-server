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

from ..get_current_me import get_current_user
from ..db import get_session

from .books_schema import CreateBook, CreateRating, ShowBook, ShowChapter, CreateChapter, CreatePage, ShowPage
from .books_models import Book, Chapter, PageModel, Rating
from .books_filter import BookFilter
app = APIRouter(prefix="/books", tags=["books"])



@app.get("")
async def get_books(ganres:list[str] = None,me = Depends(get_current_user),user_filter: Optional[BookFilter] = FilterDepends(BookFilter),session:AsyncSession = Depends(get_session)) -> Page[ShowBook]:
    query1 = user_filter.filter(select(Book).options(selectinload(Book.chapters), selectinload(Book.ratings), selectinload(Book.ganres)))
    result = await session.execute(query1)
    result = result.scalars().all()
    datas = []
    for i in result:
        data: Book = {
            "id":i.id,
            "title":i.title,
            "file_path":i.file_path,
            "author":i.author,
            "desc":i.desc,
            "writen_date":i.writen_date,
            "chapters":len(i.chapters),
            "ganres":i.ganres
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

@app.get("/with_chapters", response_model=list[ShowChapter])
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
    
@app.get("/get_pages_by_chapter")
async def get_pages_by_chapter(id_chapter:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)) -> Page[ShowPage] :
    query1 = (select(PageModel).where(PageModel.chapter_id == id_chapter))
    result = await session.execute(query1)
    return paginate(result.scalars().all())



@app.post("/rating")
async def create_rating(rating:CreateRating,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    rating = Rating(book_id = rating.book_id, rating=rating.rating, user_id=me.id)
    session.add(rating)
    await session.commit()
    await session.refresh(rating)
    return rating








@app.post("/books")
async def create_book(book:CreateBook,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    
    book = Book(**book.model_dump())
    session.add(book)
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
