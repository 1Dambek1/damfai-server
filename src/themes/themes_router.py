import json
import pathlib
from fastapi import APIRouter, Depends, HTTPException
from ..get_current_me import get_current_admin, get_current_user
from ..db import get_session

from .themes_models import Theme
from .themes_schema import CreateTheme, ShowTheme
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload




app = APIRouter(prefix="/themes", tags=["themes"])


@app.get('/all', response_model=list[ShowTheme])
async def get_themes(session:AsyncSession = Depends(get_session)):    
	themes = await session.scalars(select(Theme))
	return themes.all()

@app.post('/create/all')
async def create_themes(session:AsyncSession = Depends(get_session)): 
	BASE_DIR = pathlib.Path(__file__).resolve().parent.parent .parent
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
async def get_themes_by_user(session: AsyncSession = Depends(get_session), user = Depends(get_current_user)): 
	return user.themes

@app.get('/add/user/themes/{theme_id}', response_model=ShowTheme)
async def add_theme_to_user(theme_id: int, user = Depends(get_current_user), session: AsyncSession = Depends(get_session)): 
    # Асинхронный запрос для поиска темы по её ID
    theme = await session.scalar(select(Theme).where(Theme.id == theme_id))
    
    # Если тема не найдена, возвращаем ошибку
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    
    # Добавляем тему к пользователю, если её еще нет
    if theme not in user.themes:
        user.themes.append(theme)

    # Сохраняем изменения в базе данных
    await session.commit()

    # Обновляем данные пользователя
    await session.refresh(user)

    return theme



@app.get('/{theme_id}', response_model=ShowTheme)
async def get_theme_by_id(theme_id: int, session:AsyncSession = Depends(get_session)): 
	theme = await session.scalar(select(Theme).where(Theme.id == theme_id))
	if theme:
		return theme
	else:
		raise HTTPException(detail={"message":"theme is not exist", "status_code":404}, status_code=404)




	