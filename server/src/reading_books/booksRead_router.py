
import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from server.src.get_current_me import  get_current_user
from server.src.db import get_session
from server.src.books.books_models import Book, Chapter, PageModel
from server.src.analytics.analytics_models import PagesPerDay

from .booksRead_models import Reading_Book
from .bookRead_utils import add_minutes_and_points_for_run_per_day
from .booksRead_schema import ShowReadingBook


app = APIRouter(prefix="/books-read", tags=["books-read"])

# start to read book(redact)
@app.post("/start_to_read/{book_id}")
async def start_to_read(book_id:int,target_of_date:datetime.date = None,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
        book = await session.scalar(select(Book).where(Book.id == book_id))
        if book:
            r_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == me.id, Reading_Book.book_id == book_id))
            if r_book:
                raise HTTPException(detail={"detail":"You have already read this book", "status_code":400}, status_code=400)
                
            if target_of_date:
                r_book = Reading_Book(book_id = book.id,user_id = me.id,target_of_date = target_of_date)
            else:
                r_book = Reading_Book(book_id = book.id,user_id = me.id)
            session.add(r_book)
            await session.commit()
            return True
            
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)

# all reading books(optimize in future)
@app.get("/reading_books", response_model=list[ShowReadingBook])
async def get_reading_books(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    reading_books = await session.scalars(select(Reading_Book)
                                          .where(Reading_Book.user_id == me.id)
                                          .options(selectinload(Reading_Book.book)
                                                   .selectinload(Book.chapters)
                                                   .selectinload(Chapter.pages)))
    if reading_books:
        dataset = []
        
        for book in reading_books.all():
        # count progress
            all_pages = 0
            progress  = 0
            last_reading_page = book.last_reading_page
            
            if book.is_read:
                progress = 100
            elif last_reading_page == 0:
                last_reading_page = 0
            else:
                for page in book.book.chapters:
                    all_pages += len(page.pages)
                progress = (last_reading_page/all_pages)*100
                if progress == 100:
                    book.is_read = True
                    if book.finish_to_read is None:
                        book.finish_to_read = datetime.datetime.now().date()
                    await session.flush()
            
            data = {
                "id":book.book.id,
                "title":book.book.title,
                "author":book.book.author,
                "writen_date":book.book.writen_date,
                "progress":progress,
                "start_to_read":book.start_to_read,
                "finish_to_read":book.finish_to_read,
                "is_read":book.is_read,
                "target_of_date":book.target_of_date
            }
            dataset.append(data)
        await session.commit()
        return dataset
    raise HTTPException(detail={"detail":"You are not reading any book", "status_code":400}, status_code=400)

# read some page in reading book(redact)
@app.get("/read_page")
async def read_page(page:int,book_id:int,chapter_id:int,time_minutes:float,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    reading_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == me.id, Reading_Book.book_id == book_id))
    if reading_book:
        
        page_r = await session.scalar(select(PageModel).options(selectinload(PageModel.chapter).selectinload(Chapter.book)).where(PageModel.chapter_id == chapter_id, PageModel.numberOfPage == page))

        
        if page_r:
            if page_r.chapter.book_id == book_id:
            
                await add_minutes_and_points_for_run_per_day(time_minutes,book_id,me,session, status = reading_book.last_reading_page < page_r.numberOfPage)
                
                # add running
                count_pages_per_day = await session.scalar(select(PagesPerDay)
                                                        .where(PagesPerDay.date == datetime.datetime.now().date(), PagesPerDay.user_id == me.id))
                
                if count_pages_per_day:
                    count_pages_per_day.pages_count += 1
                else:
                    count_pages_per_day = PagesPerDay(date=datetime.datetime.now().date(),pages_count=1,user_id=me.id)
                    session.add(count_pages_per_day)
                
                if reading_book.last_reading_page < page_r.numberOfPage:
                    reading_book.last_reading_page = page_r.numberOfPage
                    await session.commit()
                    return {"status_code":200, "detail":"Page is read"}
                await session.commit()
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

# update target of reading book
@app.put("/update_target")
async def update_target(book_id:int,target_of_date:datetime.date,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    r_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == me.id, Reading_Book.book_id == book_id))
    if r_book:
        r_book.target_of_date = target_of_date
        await session.commit()
        return True
    raise HTTPException(detail={"detail":"Reading book is not exist", "status_code":400}, status_code=400)

# get target of reading book
@app.get("/target/{book_id}")
async def get_target(book_id:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    r_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == me.id, Reading_Book.book_id == book_id))
    if r_book:
        return {"target_of_date":r_book.target_of_date, "book_id": book_id}
    
    raise HTTPException(detail={"detail":"Reading book is not exist", "status_code":400}, status_code=400)
   