
import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .emotes_books_schema import SaveEmoteEnum


from ..get_current_me import  get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book
app = APIRouter(prefix="/emotes-books", tags=["emotes-books"])

@app.get("/all")
async def get_all_emotes_books(user: User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
	if user.emote:
		books = await session.scalars(select(Book).where(Book.emote == user.emote))
		return books.all()

	return []



@app.put("/save/emote") 
async def save_emote(data:SaveEmoteEnum,user: User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
	user.emote = data.emote
	await session.commit()
	await session.refresh(user)
	return data





