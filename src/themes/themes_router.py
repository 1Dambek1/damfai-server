
import json
import pathlib
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..get_current_me import get_current_admin, get_current_user, get_current_id
from ..db import get_session
from ..app_auth.auth_models import User

from .themes_models import Theme
from .themes_schema import CreateTheme, ShowTheme

app = APIRouter(prefix="/themes", tags=["themes"])


@app.get('/all', response_model=list[ShowTheme])
async def get_themes(session:AsyncSession = Depends(get_session)):    
	themes = await session.scalars(select(Theme))

	return themes.all()

@app.post('/create/all')
async def create_themes(session:AsyncSession = Depends(get_session)): 
	BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
	themes_data_url = BASE_DIR / 'data' / 'themes.json'
	
	with open(themes_data_url, "r", encoding='utf-8') as f:
		themes = json.load(f)	

	objects = [Theme(**i) for i in themes]

	try:
		session.add_all(objects)
		await session.commit()
	except Exception as e:
		await session.rollback()
		raise e

	return True

@app.post('/create', response_model=ShowTheme)
async def create_theme(data: CreateTheme, _ = Depends(get_current_admin), session: AsyncSession = Depends(get_session)): 
	data_dict = data.model_dump()
	theme = Theme(**data_dict)
	session.add(theme)	
	await session.commit()
	await session.refresh(theme)
	return theme


@app.get('/user/themes', response_model=list[ShowTheme])
async def get_themes_by_user(user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 
	user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.themes)))
	return user.themes

@app.get('/add/user/themes/{theme_id}', response_model=ShowTheme)
async def add_theme_to_user(theme_id: int, user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 

	theme = await session.scalar(select(Theme).where(Theme.id == theme_id))
	user: User = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.themes)))

	
	if not theme:
		raise HTTPException(status_code=404, detail="Theme not found")
	if theme not in user.themes and user.balance >= theme.price:
		user.balance = user.balance - theme.price
		user.themes.append(theme)
	else:
		raise HTTPException(status_code=400, detail="Not enough money or theme already exist")
	await session.commit()
	await session.refresh(user)
	return theme

@app.delete('/remove/user/themes/{theme_id}')
async def remove_theme_from_user(theme_id: int, user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 

		theme = await session.scalar(select(Theme).where(Theme.id == theme_id))
		user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.themes)))
		if not theme:
			raise HTTPException(status_code=404, detail="theme not found")
		if theme in user.themes:
			user.balance = user.balance + theme.price
			user.themes.remove(theme)
		await session.commit()
		await session.refresh(user)	
		return True

@app.get('/balance_increase')
async def balance_increase(balance: int, user_id = Depends(get_current_id),session:AsyncSession = Depends(get_session)):
	user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.themes)))
	if user:
		user.balance = user.balance + balance
		await session.commit()
		await session.refresh(user)
		return user
	raise HTTPException(detail={"message":"user is not exist", "status_code":404}, status_code=404)


@app.get('/{theme_id}', response_model=ShowTheme)
async def get_theme_by_id(theme_id: int, session:AsyncSession = Depends(get_session)): 
	theme = await session.scalar(select(Theme).where(Theme.id == theme_id))
	if theme:
		return theme
	else:
		raise HTTPException(detail={"message":"theme is not exist", "status_code":404}, status_code=404)




	