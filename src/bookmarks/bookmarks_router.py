
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .bookmarks_schema import ShowBookmark, ShowFavourite
from .bookmarsk_models import BookmarkUser, FavouriteUser

from ..get_current_me import  get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Chapter, PageModel

app = APIRouter(prefix="/bookmarks", tags=["bookmarks"])



# get bookmarks(redact+-)
@app.get("/", response_model=list[ShowBookmark])
async def get_bookmarks(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.id == me.id).options(selectinload(User.bookmarks_on_page).selectinload(PageModel.chapter).selectinload(Chapter.book)))
    dataset  = []
    for i in user.bookmarks_on_page:
        data = {
            "id":i.chapter.book.id,
            "title":i.chapter.book.title,
            "author":i.chapter.book.author,
            "desc":i.chapter.book.desc,
            "writen_date":i.chapter.book.writen_date,
            "age_of_book":i.chapter.book.age_of_book,
            "id_current_chapter":i.chapter_id,
            "current_page":i.id,
            "current_number_of_page": i.numberOfPage
        }
        dataset.append(data)
    return dataset

# get favourite(redact)
@app.get("/favourite", response_model=list[ShowFavourite])
async def get_favourite(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalar(select(User).where(User.id == me.id).options(selectinload(User.favourite_books)))
    return favourite.favourite_books




# create favourite(redact)
@app.put("/favourite/{book_id}")
async def favourite_update(book_id:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalar(select(FavouriteUser).where(FavouriteUser.user_id == me.id, FavouriteUser.book_id == book_id))
    if favourite:
        await session.delete(favourite)
        await session.commit()
        return False
    favourite = FavouriteUser(book_id=book_id, user_id=me.id)
    session.add(favourite)
    await session.commit()
    return True

#  create bookmarks(redact)
@app.put("/{page_id}")
async def bookmarks_update(page_id:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    bookmark = await session.scalar(select(BookmarkUser).where(BookmarkUser.user_id == me.id, BookmarkUser.page_id == page_id))
    if bookmark:
        await session.delete(bookmark)
        await session.commit()
        return False
    bookmark = BookmarkUser(page_id=page_id, user_id=me.id)
    session.add(bookmark)
    await session.commit()
    return True


 
#  check bookmarks(redact)
@app.get("/is_bookmark/{page_id}")
async def is_bookmark(page_id:int, me:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    bookmark = await session.scalar(select(BookmarkUser).where(BookmarkUser.user_id == me.id, BookmarkUser.page_id == page_id))
    if bookmark:
        return {"is_bookmark":True}
    return {"is_bookmark":False}
  
#  check favourite(redact)  
@app.get("/is_favourite/{book_id}")
async def is_favourite(book_id:int, me:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalar(select(FavouriteUser).where(FavouriteUser.user_id == me.id, FavouriteUser.book_id == book_id)) 
    if favourite:
        return {"is_favourite":True}
    return {"is_favourite":False}