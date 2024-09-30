from fastapi import APIRouter, Depends

from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session

from .bookmarks_schema import ShowUserWithBookMarks, ShowUserWithFavourite

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload, aliased

app = APIRouter(prefix="/bookmarks", tags=["bookmarks"])



@app.get("/", response_model=ShowUserWithBookMarks)
async def get_bookmarks(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    bookmarks = await session.scalars(select(User).where(User.id == user_id).options(selectinload(User.bookmarks)))
    return bookmarks.all()

@app.get("/favourite", response_model=ShowUserWithFavourite)
async def get_bookmarks(user_id = Depends(get_current_id),me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    favourite = await session.scalars(select(User).where(User.id == user_id).options(selectinload(User.favourite)))
    return favourite.all()


