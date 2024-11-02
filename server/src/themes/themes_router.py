
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from    server.src.get_current_me import  get_current_id
from    server.src.db import get_session
from    server.src.app_auth.auth_models import User

from .themes_models import Theme
from .themes_schema import ShowTheme

app = APIRouter(prefix="/themes", tags=["themes"])

# get all themes
@app.get('/all', response_model=list[ShowTheme])
async def get_themes(session:AsyncSession = Depends(get_session)):    
	themes = await session.scalars(select(Theme))

	return themes.all()

# user themes
@app.get('/user/themes', response_model=list[ShowTheme])
async def get_themes_by_user(user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 
	user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.themes)))
	return user.themes

# current theme by id
@app.get('/{theme_id}', response_model=ShowTheme)
async def get_theme_by_id(theme_id: int, session:AsyncSession = Depends(get_session)): 
	theme = await session.scalar(select(Theme).where(Theme.id == theme_id))
	if theme:
		return theme
	else:
		raise HTTPException(detail={"message":"theme is not exist", "status_code":404}, status_code=404)

