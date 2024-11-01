
import json
import pathlib
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..get_current_me import get_current_admin, get_current_user, get_current_id
from ..db import get_session
from ..app_auth.auth_models import User
from ..themes.themes_models import Theme

from .shop_schema import  ShowTheme


app = APIRouter(prefix = "/shop", tags = ["shop"])


@app.get('/balance_increase')
async def balance_increase(balance: int, user_id = Depends(get_current_id),session:AsyncSession = Depends(get_session)):
	user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.themes)))
	if user:
		user.balance = user.balance + balance
		await session.commit()
		await session.refresh(user)
		return user
	raise HTTPException(detail={"message":"user is not exist", "status_code":404}, status_code=404)




@app.get('/buy/user/themes/{theme_id}', response_model=ShowTheme)
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

@app.delete('/sell/user/themes/{theme_id}')
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

