import shutil
from typing import Optional
import os 

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from fastapi_pagination import  add_pagination,Page,paginate
from fastapi_pagination.utils import disable_installed_extensions_check
disable_installed_extensions_check()

from fastapi_filter import FilterDepends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from ..get_current_me import get_current_user
from ..db import get_session

from .books_schema import CreateBook, CreateRating, ShowBook, CreateChapter, CreatePage, ShowPage, ShowGanres,ShowBookWithChapters
from .books_models import Book, Chapter, PageModel, Rating, Ganre
from .books_filter import BookFilter


app = APIRouter(prefix="/books", tags=["books"])


# ---------------------work with book---------------------
@app.get("/book")
async def get_book(id_book:int, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        return book
    else:
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)

# img for book
@app.get("/img/{id_book}")
async def main(id_book:int, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        if book.file_path:
            return FileResponse(f"images/books_img/{book.file_path}")
    else:
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)

# get filter books with pagintation
@app.post("")
async def get_books(ganres:list[int],rating__lte:float = None, rating__gte:float = None,user_filter: Optional[BookFilter] = FilterDepends(BookFilter),session:AsyncSession = Depends(get_session))-> Page[ShowBook] :
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

# get chapters of book
@app.get("/chapters/{id_book}", response_model=ShowBookWithChapters)
async def get_books_with_chapters(id_book:int,session:AsyncSession = Depends(get_session)):
    result = await session.scalar((select(Book).options(selectinload(Book.chapters).selectinload(Chapter.pages)).where(Book.id == id_book)))
    datas = []
    for i in result.chapters:
            data = {
                "id":i.id,
                "title":i.title,
                "numberOfChapter":i.numberOfChapter,
                "pages":len(i.pages),
            }

            datas.append(data)
    data_set = {"id":result.id,"title":result.title,"author":result.author, "chapters":datas}
    return data_set

# get pages of chapter with pagintation
@app.get("/get_pages_by_chapter/{id_chapter}")
async def get_pages_by_chapter(id_chapter:int, page:int, me = Depends(get_current_user),session:AsyncSession = Depends(get_session))  :
    page = await session.scalar(select(PageModel).where(PageModel.chapter_id == id_chapter, PageModel.numberOfPage == page))
    return page

#  ---------------------work with rating--------------s-------


# rate book 
@app.post("/book/rating")
async def create_rating(rating_data:CreateRating,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    rating_your = await session.scalar(select(Rating).where(Rating.book_id == rating_data.book_id, Rating.user_id == me.id))
    if rating_your:
        rating_your.rating = rating_data.rating
        await session.commit()
        await session.refresh(rating_your)
        return rating_your
    else:
        try:
            rating = Rating(book_id = rating_data.book_id, rating=rating_data.rating, user_id=me.id)
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


# all ganres
@app.get("/ganres/all", response_model = list[ShowGanres])
async def ganres(session:AsyncSession = Depends(get_session)):
    ganres = await session.scalars(select(Ganre))
    return ganres.all()


#  ---------------------work with create(DEBUG)---------------------


# create ganre
@app.post("/ganres/create")
async def create_ganre(ganre:str,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    ganre_m = Ganre(ganre=ganre)
    session.add(ganre_m)
    await session.commit()
    await session.refresh(ganre_m) 
    return ganre_m

# create book
@app.post("/create")
async def create_book(book_data:CreateBook = Depends(CreateBook), me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    book:Book= Book(title = book_data.title, author = book_data.author, desc = book_data.desc, writen_date = book_data.writen_date, age_of_book = book_data.age_of_book)
    for i in book_data.ganres:
        ganre = await session.scalar(select(Ganre).where(Ganre.id == i))
        if ganre:
            book.ganres.append(ganre)

    session.add(book)
    
    await session.commit()
    await session.refresh(book)
    return book

# create img for book
@app.post("/create/img/{id_book}")
async def create_img(id_book:int,file:UploadFile = File(...), me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        file_name = str(book.id) + ".jpg"
        file_path = f"images/books_img/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        book.file_path = file.filename
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
    raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)

# create chapter   
@app.post("/chapter/create")
async def create_chapter(chapter_data:list[CreateChapter],me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):  

    for i in chapter_data:
        chapter = Chapter(title = i.title, numberOfChapter = i.numberOfChapter, book_id = i.book_id)

        session.add(chapter)
    await session.commit()
    
    return True

# create pages
@app.post("/pages/create")
async def update_pages(pages_data:list[CreatePage],me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    for i in pages_data:
        page = PageModel(numberOfPage = i.numberOfPage, text = i.text, chapter_id = i.chapter_id)
        session.add(page)
    await session.commit()
    return True
add_pagination(app)  




