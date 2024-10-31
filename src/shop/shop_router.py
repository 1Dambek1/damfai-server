
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



