

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi_pagination import  add_pagination,Page,paginate
from fastapi_pagination.utils import disable_installed_extensions_check
disable_installed_extensions_check()
from fastapi_filter import FilterDepends

from ..get_current_me import get_current_user
from ..db import get_session

from .books_schema import  CreateRating, ShowBook, ShowGanres,ShowBookWithChapters
from .books_models import Book, Chapter, PageModel, Rating, Ganre
from .books_filter import BookFilter

app = APIRouter(prefix="/books", tags=["books"])


# ---------------------work with book---------------------
@app.get("/book")
async def get_book(id_book:int, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        return book
    raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)

# get img for book
@app.get("/img/{id_book}")
async def main(id_book:int, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        if book.file_path:
            return FileResponse(f"images/books_img/{book.file_path}")
    raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)



# get filter books with pagintation
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
                            "zip_text":i.zip_text
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
    dataset = {"id":result.id,"title":result.title,"author":result.author, "chapters":datas}
    return dataset

# get pages of chapter with pagintation
@app.get("/get_pages_by_chapter/{id_chapter}")
async def get_pages_by_chapter(id_chapter:int, page:int, me = Depends(get_current_user),session:AsyncSession = Depends(get_session))  :
    page = await session.scalar(select(PageModel).where(PageModel.chapter_id == id_chapter, PageModel.numberOfPage == page))
    return page

#  ---------------------work with rating---------------------


# rate book 
@app.put("/book/rating")
async def create_rating(rating_data:CreateRating,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    rating_your = await session.scalar(select(Rating).where(Rating.book_id == rating_data.book_id, Rating.user_id == me.id))
    if rating_your:
        rating_your.rating = rating_data.rating
        await session.commit()
        await session.refresh(rating_your)
        return rating_your

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

add_pagination(app)