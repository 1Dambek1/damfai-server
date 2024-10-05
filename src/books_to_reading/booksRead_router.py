import datetime
from fastapi import APIRouter, Depends, HTTPException

from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, Chapter, PageModel

from  .booksRead_models import Reading_Book
from .booksRead_schema import ShowReadingBook

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload, aliased


app = APIRouter(prefix="/books-read", tags=["books-read"])

# start to read book
@app.post("/start_to_read/{book_id}")
async def start_to_read(book_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.reading_books)))
    if user:
        book = await session.scalar(select(Book).where(Book.id == book_id))
        if book:
            user.reading_books.append(book)
            await session.commit()
            return True
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"User is not exist", "status_code":400}, status_code=400)

# all reading books
@app.get("/reading_books")
async def get_reading_books(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    reading_books = await session.scalars(select(Reading_Book).where(Reading_Book.user_id == user_id).options(selectinload(Reading_Book.book).selectinload(Book.chapters).selectinload(Chapter.pages)))
    if reading_books:
        dataset = []
        for i in reading_books.all():
            all_pages = 0
            progress  = 0
            last_reading_page = i.last_reading_page

            if i.is_read == True:
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
                "book_id":i.book.id,
                "title":i.book.title,
                "author":i.book.author,
                "writen_date":i.book.writen_date,
                "progress":progress,
                "start_to_read":i.start_to_read,
                "finish_to_read":i.finish_to_read
            }
            dataset.append(data)
        await session.commit()
        return dataset
    raise HTTPException(detail={"detail":"User is not exist", "status_code":400}, status_code=400)

# read some page in reading book
@app.get("/read_page")
async def read_page(page_id:int,book_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    r_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == user_id, Reading_Book.book_id == book_id))
    if r_book:

        page = await session.scalar(select(PageModel).where(PageModel.id == page_id).options(selectinload(PageModel.chapter).selectinload(Chapter.book)))
        if page:
            if page.chapter.book_id == book_id:
                if r_book.last_reading_page < page.numberOfPage:
                    r_book.last_reading_page = page.numberOfPage
                    await session.commit()
                    return {"status_code":200, "detail":"Page is read"}
                return {"status_code":200, "detail":"You still read this book"}
        raise HTTPException(detail={"detail":"Page is not exist", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"Reading book is not exist", "status_code":400}, status_code=400)

# finish reading book
@app.get("/finish_book")
async def finish_book(book_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    r_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == user_id, Reading_Book.book_id == book_id))
    if r_book:
        r_book.is_read = True
        if r_book.finish_to_read is None:
            r_book.finish_to_read = datetime.datetime.now().date()
        await session.commit()
        return True
    
    raise HTTPException(detail={"detail":"Reading book is not exist", "status_code":400}, status_code=400)

