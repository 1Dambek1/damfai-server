
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends,  HTTPException
from fastapi.responses import FileResponse


from server.src.get_current_me import get_current_user
from server.src.db import get_session
from server.src.utils.common_schema import ShowBook
from server.src.reading_books.booksRead_models import Reading_Book

from .books_schema import  CreateRating, ShowGanres,ShowBookWithChapters,ShowPage
from .books_models import Book, Chapter, PageModel, Rating, Ganre

app = APIRouter(prefix="/books", tags=["books"])


# get book by id(redact)
@app.get("/get/book/{id_book}", response_model=ShowBook)
async def get_book(id_book:int, session:AsyncSession = Depends(get_session)):
    books_query = (select(Book,func.coalesce(func.avg(Rating.rating), 0).label("average_rating"),func.count(Chapter.id).label("chapters"))
                   .join(Rating, isouter=True)
                   .join(Chapter, isouter=True)
                   .options(selectinload(Book.ganres))
                   .where(Book.id == id_book)
                   .group_by(Book.id))
    result = await session.execute(books_query)
    result = result.one_or_none()
    if result:
        book, average_rating, chapters = result
        book = book.__dict__
        book["ganres"] = [ganre.ganre for ganre in book["ganres"]]
        book["ratings"] = average_rating
        book["chapters"] = chapters
        return book
    raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)


# get img book by id(redact)
@app.get("/get/book/img/{id_book}")
async def get_image_book(id_book:int, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        if book.file_path:
            return FileResponse(f"images/books_img/{book.file_path}")
        raise HTTPException(detail={"detail":"Book do not have image", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)


# get chapter of book by id(redact)
@app.get("/get/book/chapters/{id_book}", response_model=ShowBookWithChapters)
async def get_books_with_chapters(id_book:int,session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if not book:
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)
    
    query = select(Chapter,func.count(PageModel.id),func.max(PageModel.numberOfPage)).join(PageModel, isouter=True).where(Chapter.book_id == id_book).group_by(Chapter.id)
    
    result = await session.execute(query)
    result = result.all()
    
    if result:
        return {"title":book.title,
                "author":book.author,
                "id":book.id,
                "chapters":[{"id":chapter.id,
                             "title":chapter.title,
                             "numberOfChapter":chapter.numberOfChapter,
                             "pages":count_page,
                             'lastNumberOfPage': last_page_number if last_page_number else None
                             } for chapter, count_page, last_page_number in result]}
    raise HTTPException(detail={"detail":"Chapters is not exist", "status_code":400}, status_code=400)


# get page of chapter(redact)
@app.get("/get_pages_by_chapter/{id_chapter}", response_model=ShowPage)
async def get_pages_by_chapter(id_book:int,id_chapter:int, page:int, me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    r_book = await session.scalar(select(Reading_Book).where(Reading_Book.book_id == id_book))
    if r_book:
        page = await session.scalar(select(PageModel).where(PageModel.chapter_id == id_chapter, PageModel.numberOfPage == page))
        return page
    raise HTTPException(detail={"status_code":403, "detail":"You do not read this book"}, status_code=403)

#  ---------------------work with rating---------------------

# rate book (redact)
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
    return True


#  ---------------------work with ganres---------------------

# all ganres
@app.get("/ganres/all", response_model = list[ShowGanres])
async def ganres(session:AsyncSession = Depends(get_session)):
    ganres = await session.scalars(select(Ganre))
    return ganres.all()


