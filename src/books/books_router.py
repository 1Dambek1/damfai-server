import shutil
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


# ---------------------work with book---------------------
@app.get("/img")
async def main(id_book:str, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        return FileResponse(f"{book.file_path}")
    raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)

@app.post("")
async def get_books(ganres:list[int],rating__lte:float = None, rating__gte:float = None,me = Depends(get_current_user),user_filter: Optional[BookFilter] = FilterDepends(BookFilter),session:AsyncSession = Depends(get_session))-> Page[ShowBook] :
    query1 = user_filter.filter(select(Book).options(selectinload(Book.chapters), selectinload(Book.ratings), selectinload(Book.ganres)))
    result = await session.execute(query1)
    result = result.scalars().all()
    datas = []
    
    for i in result:
            i:Book
            is_good = True  
            mine_ganres = [i2.id for i2 in i.ganres]                     
            for i2 in ganres:
                if not i2 in mine_ganres:
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
                            "age_of_book": i.age_of_book
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

@app.get("/chapters/{id_book}", response_model=list[ShowChapter])
async def get_books_with_chapters(id_book:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    query1 = (select(Chapter).options(selectinload(Chapter.pages)).where(Chapter.book_id == id_book))
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



#  ---------------------work with rating---------------------


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



#  ---------------------work with ganres---------------------

@app.get("/ganres/all", response_model = list[ShowGanres])
async def ganres(me = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    ganres = await session.scalars(select(Ganre))
    return ganres.all()

#  ---------------------work with create(DEBUG)---------------------

@app.post("/ganres/create")
async def create_ganre(ganre:str,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    ganre_m = Ganre(ganre=ganre)
    session.add(ganre_m)
    await session.commit()
    await session.refresh(ganre_m) 
    return ganre_m

@app.post("/create")
async def create_book(book_data:CreateBook = Depends() ,file:UploadFile = File(...), me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    book:Book= Book(title = book_data.title, author = book_data.author, desc = book_data.desc, writen_date = book_data.writen_date, age_of_book = book_data.age_of_book)
    for i in book_data.ganres:
        ganre = await session.scalar(select(Ganre).where(Ganre.id == i))
        if ganre:
            book.ganres.append(ganre)
    file_name = str(book_data.title)
    file_path = f"books_img/{file_name}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    book.file_path = file_path
    session.add(book)
    
    await session.commit()
    await session.refresh(book)
    return book

@app.post("/chapter/create")
async def create_chapter(chapter_data:list[CreateChapter],me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):  

    for i in chapter_data:
        chapter = Chapter(title = i.title, numberOfChapter = i.numberOfChapter, book_id = i.book_id)

        session.add(chapter)
    await session.commit()
    
    return True

@app.post("/pages/create")
async def update_pages(pages_data:list[CreatePage],me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    for i in pages_data:
        page = PageModel(numberOfPage = i.numberOfPage, text = i.text, chapter_id = i.chapter_id)
        session.add(page)
    await session.commit()
    return True
add_pagination(app)  



