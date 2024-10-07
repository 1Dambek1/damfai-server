from fastapi import APIRouter, Depends, HTTPException

from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, Chapter, PageModel

from .bookmarks_schema import ShowBookmark, ShowFavourite
from .bookmarsk_models import BookmarkUser, FavouriteUser

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload, aliased

app = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

#  ---------------------get bookmarks and favourite---------------------

# get bookmarks
@app.get("/", response_model=list[ShowBookmark])
async def get_bookmarks(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.bookmarks_on_page).selectinload(PageModel.chapter).selectinload(Chapter.book)))

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
            "current_page":i.id
        }
        dataset.append(data)
    return dataset


# get favourite
@app.get("/favourite", response_model=list[ShowFavourite])
async def get_favourite(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.favourite_books)))
    return favourite.favourite_books


#  ---------------------create bookmarks and favourite---------------------

# create favourite
@app.put("/favourite")
async def favourite_update(book_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalar(select(FavouriteUser).where(FavouriteUser.user_id == user_id, FavouriteUser.book_id == book_id))
    if favourite:
        await session.delete(favourite)
        await session.commit()
        return True
    else:
        favourite = FavouriteUser(book_id=book_id, user_id=user_id)
        session.add(favourite)
        await session.commit()
        return True

#  create bookmarks
@app.put("")
async def bookmarks_update(page_id:int,user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    bookmark = await session.scalar(select(BookmarkUser).where(BookmarkUser.user_id == user_id, BookmarkUser.page_id == page_id))
    if bookmark:
        await session.delete(bookmark)
        await session.commit()
        return True
    else:
        bookmark = BookmarkUser(page_id=page_id, user_id=user_id)
        session.add(bookmark)
        await session.commit()
        return True


#  ---------------------check is bookmark and favourite---------------------
 
@app.get("/is_bookmark/{page_id}")
async def is_bookmark(page_id:int,user_id:int = Depends(get_current_id), user:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    bookmark = await session.scalar(select(BookmarkUser).where(BookmarkUser.user_id == user_id, BookmarkUser.page_id == page_id))
    if bookmark:
        return {"is_bookmark":True}
    else:
        return {"is_bookmark":False}
    
@app.get("/is_favourite/{book_id}")
async def is_bookmark(book_id:int,user_id:int = Depends(get_current_id), user:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalar(select(FavouriteUser).where(FavouriteUser.user_id == user_id, FavouriteUser.book_id == book_id)) 
    if favourite:
        return {"is_favourite":True}
    else:
        return {"is_favourite":False}