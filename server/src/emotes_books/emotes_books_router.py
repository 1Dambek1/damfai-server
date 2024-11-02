
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.src.get_current_me import  get_current_user
from server.src.app_auth.auth_models import User
from server.src.db import get_session
from server.src.books.books_models import Book

from .emotes_books_schema import SaveEmoteEnum

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





