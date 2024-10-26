
import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .booksRead_models import Reading_Book

from ..get_current_me import  get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, Chapter, PageModel
from ..analytics.analytics_models import PagesPerDay
from fastapi.responses import FileResponse

app = APIRouter(prefix="/books-read", tags=["books-read"])

# start to read book(redact)
@app.post("/start_to_read/{book_id}")
async def start_to_read(book_id:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
        book = await session.scalar(select(Book).where(Book.id == book_id))
        if book:
            me.reading_books.append(book)
            await session.commit()
            return True
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)

# all reading books(optimize in future)
@app.get("/reading_books")
async def get_reading_books(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    reading_books = await session.scalars(select(Reading_Book)
                                          .where(Reading_Book.user_id == me.id)
                                          .options(selectinload(Reading_Book.book)
                                                   .selectinload(Book.chapters)
                                                   .selectinload(Chapter.pages)))
    if reading_books:
        dataset = []
        
        for i in reading_books.all():
        # count progress
            all_pages = 0
            progress  = 0
            last_reading_page = i.last_reading_page
            
            if i.is_read:
                progress = 100
            elif last_reading_page == 0:
                last_reading_page = 0
            else:
                for i2 in i.book.chapters:
                    all_pages += len(i2.pages)
                progress = (last_reading_page/all_pages)*100
                if progress == 100:
                    i.is_read = True
                    if i.finish_to_read is None:
                        i.finish_to_read = datetime.datetime.now().date()
                    await session.flush()
            
            data = {
                "id":i.book.id,
                "id":i.book.id,
                "title":i.book.title,
                "author":i.book.author,
                "writen_date":i.book.writen_date,
                "progress":progress,
                "start_to_read":i.start_to_read,
                "finish_to_read":i.finish_to_read,
                "is_read":i.is_read
            }
            dataset.append(data)
        await session.commit()
        return dataset
    raise HTTPException(detail={"detail":"You are not reading any book", "status_code":400}, status_code=400)

# read some page in reading book(redact)
@app.get("/read_page")
async def read_page(page_id:int,book_id:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    reading_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == me.id, Reading_Book.book_id == book_id))
    if reading_book:
        reading_page = await session.scalar(select(PageModel).where(PageModel.id == page_id).options(selectinload(PageModel.chapter).selectinload(Chapter.book)))
        if reading_page and reading_page.chapter.book_id == book_id:
            
            # count pages per day
            count_pages_per_day = await session.scalar(select(PagesPerDay).where(PagesPerDay.date == datetime.datetime.now().date(), PagesPerDay.user_id == me.id))
            if count_pages_per_day:
                count_pages_per_day.pages_count += 1
            else:
                count_pages_per_day = PagesPerDay(date=datetime.datetime.now().date(),pages_count=1,user_id=me.id)
                session.add(count_pages_per_day)
            
            if reading_book.last_reading_page < reading_page.numberOfPage:
                reading_book.last_reading_page = reading_page.numberOfPage
                await session.commit()
                return {"status_code":200, "detail":"Page is read"}
            return {"status_code":200, "detail":"You still read this book"}
        raise HTTPException(detail={"detail":"Page is not exist", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"Reading book is not exist", "status_code":400}, status_code=400)

# finish reading book
@app.get("/finish_book")
async def finish_book(book_id:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    r_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == me.id, Reading_Book.book_id == book_id))
    if r_book:
        r_book.is_read = True
        if r_book.finish_to_read is None:
            r_book.finish_to_read = datetime.datetime.now().date()
        await session.commit()
        return True
    
    raise HTTPException(detail={"detail":"Reading book is not exist", "status_code":400}, status_code=400)

logging.basicConfig(level=logging.ERROR)



