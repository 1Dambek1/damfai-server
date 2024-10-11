import datetime
import logging
import os
from fastapi import APIRouter, Depends, HTTPException
import shutil
from ..config  import config
import requests
from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, Chapter, PageModel
from ..analytics.analytics_models import PagesPerDay
from fastapi.responses import FileResponse

from  .booksRead_models import Reading_Book

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


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
    raise HTTPException(detail={"detail":"User is not exist", "status_code":400}, status_code=400)

# read some page in reading book
@app.get("/read_page")
async def read_page(page_id:int,book_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    r_book = await session.scalar(select(Reading_Book).where(Reading_Book.user_id == user_id, Reading_Book.book_id == book_id))
    if r_book:

        page = await session.scalar(select(PageModel).where(PageModel.id == page_id).options(selectinload(PageModel.chapter).selectinload(Chapter.book)))
        if page:
            if page.chapter.book_id == book_id:
                page_r = await session.scalar(select(PagesPerDay).where(PagesPerDay.date == datetime.datetime.now().date(), PagesPerDay.user_id == user_id))
                if page_r:
                    page_r.pages_count += 1
                else:
                    page_r = PagesPerDay(date=datetime.datetime.now().date(),pages_count=1,user_id=user_id)
                    session.add(page_r)
                
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

logging.basicConfig(level=logging.ERROR)

@app.get('/speech/{book_id}')
async def speech(book_id: int, me = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == book_id))

    if book:
        try:
            url = config.speech_data.SPEECH_URL
            token = config.speech_data.SPEECH_ACCESS_TOKEN
            headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'application/ssml'}
            data = f"Привет, {me.name}!"

            response = requests.post(url, headers=headers, data=data, verify=False)
            if response.status_code == 200:
                wav_data = response.content

                file_name = f"book_{book_id}.wav"
                file_path = os.path.join('audios/books', file_name)

                with open(file_path, "wb") as f:
                    f.write(wav_data)

                return {"audioUrl": f"{file_path}"}
                
            else:
                logging.error(f"Request failed with status code {response.status_code}")
                return HTTPException(status_code=400, detail="Bad request failed")

        except requests.exceptions.SSLError as ssl_error:
            logging.error(f"SSL Error occurred: {ssl_error}")
        except requests.exceptions.RequestException as req_error:
            logging.error(f"Request Error: {req_error}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    
    raise HTTPException(detail={"detail":"Book is not exists", "status_code":404}, status_code=404)




