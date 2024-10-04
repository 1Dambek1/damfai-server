from fastapi import APIRouter, Depends, HTTPException

from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, PageModel

from .bookmarks_schema import ShowUserWithBookMarks, ShowUserWithFavourite
from .bookmarsk_models import FavouriteUser, BookmarkUser

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload, aliased

app = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

#  ---------------------get bookmarks and favourite---------------------

# get bookmarks
@app.get("/")
async def get_bookmarks(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    bookmarks = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.bookmarks_on_page)))
    return bookmarks

# get favourite
@app.get("/favourite")
async def get_bookmarks(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.favourite_books)))
    return favourite


#  ---------------------create bookmarks and favourite---------------------

# create favourite
@app.post("/favourite")
async def favourite(book_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user:User = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.favourite_books)))
    if user:
        book = await session.scalar(select(Book).where(Book.id == book_id))
        if book:
            user.favourite_books.append(book)
            await session.commit()
            return {"data":"Book is added to favourite"}
            
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"user is not exist", "status_code":400}, status_code=400)

#  create bookmarks
@app.post("")
async def favourite(page_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user:User = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.bookmarks_on_page)))
    if user:
        page = await session.scalar(select(PageModel).where(PageModel.id == page_id))
        if page:
            user.bookmarks_on_page.append(page)
            await session.commit()
            return {"data":"Page is added to bookmarks"}
            
        raise HTTPException(detail={"detail":"Page is not exist", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"user is not exist", "status_code":400}, status_code=400)



# delete bookmarks
@app.delete("")
async def favourite(page_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user:User = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.bookmarks_on_page)))
    if user:
        page = await session.scalar(select(PageModel).where(PageModel.id == page_id))
        if page:
            user.bookmarks_on_page.remove(page)
            await session.commit()
            return {"data":"Page is deleted from bookmarks"}
            
        raise HTTPException(detail={"detail":"Page is not exist", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"user is not exist", "status_code":400}, status_code=400)

@app.delete("/favourite")
async def favourite(book_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user:User = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.favourite_books)))
    if user:
        book = await session.scalar(select(Book).where(Book.id == book_id))
        if book:
            user.favourite_books.remove(book)
            await session.commit()
            return {"data":"Book is deleted from favourite"}
            
        raise HTTPException(detail={"detail":"Book is not exist", "status_code":400}, status_code=400)
    raise HTTPException(detail={"detail":"user is not exist", "status_code":400}, status_code=400)


# @app.get("/tests")
# async def test(session:AsyncSession = Depends(get_session)):
#     test1 = await session.scalars(select(FavouriteUser))
#     test2 = await session.scalars(select(BookmarkUser)) 

#     return {"data1":test1.all(), "data2":test2.all()}