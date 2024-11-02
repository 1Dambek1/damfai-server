from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.src.get_current_me import  get_current_user
from server.src.db import get_session
from server.src.themes.themes_models import Theme

from .shop_schema import  ShowTheme


app = APIRouter(prefix = "/shop", tags = ["shop"])

# add balance
@app.get('/balance_increase')
async def balance_increase(balance: int, me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):

	me.balance = me.balance + balance
	await session.commit()
	return True

# but theme
@app.get('/buy/user/themes/{theme_id}', response_model=ShowTheme)
async def add_theme_to_user(theme_id: int, user = Depends(get_current_user), session: AsyncSession = Depends(get_session)): 

	theme = await session.scalar(select(Theme).where(Theme.id == theme_id))

	
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

# sell theme
@app.delete('/sell/user/themes/{theme_id}')
async def remove_theme_from_user(theme_id: int, user = Depends(get_current_user), session: AsyncSession = Depends(get_session)): 

		theme = await session.scalar(select(Theme).where(Theme.id == theme_id))
		if not theme:
			raise HTTPException(status_code=404, detail="theme not found")
		if theme in user.themes:
			user.balance = user.balance + theme.price
			user.themes.remove(theme)
		await session.commit()
		await session.refresh(user)	
		return True



	
