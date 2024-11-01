
import json
import pathlib
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..get_current_me import get_current_admin, get_current_id
from ..db import get_session
from ..app_auth.auth_models import User

from .extensions_models import Extension
from .extensions_schema import CreateExtension, ShowExtension

app = APIRouter(prefix="/extensions", tags=["extensions"])

# get all extensions
@app.get('/all', response_model=list[ShowExtension])
async def get_extensions(session:AsyncSession = Depends(get_session)):    
	extensions = await session.scalars(select(Extension))
	return extensions.all()



@app.get('/user/extensions', response_model=list[ShowExtension])
async def get_extensions_by_user(user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 
	user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.extensions)))
	return user.extensions

@app.get('/by-slug')
async def get_extension_by_slug(slug: str, session:AsyncSession = Depends(get_session)): 
	extension = await session.scalar(select(Extension).where(Extension.slug == slug))
	if extension:
		return extension
	else:
		raise HTTPException(detail={"message":"extension is not exist", "status_code":404}, status_code=404)


@app.post('/add/user/extensions/{extension_id}', response_model=ShowExtension)
async def add_extension_to_user(extension_id: int, user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 
    ex = await session.scalar(select(Extension).where(Extension.id == extension_id))
	
    user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.extensions)))
    
    
    if not ex:
        raise HTTPException(status_code=404, detail="extension not found")
    
    if ex not in user.extensions:
        user.extensions.append(ex)

    # Сохраняем изменения в базе данных
    await session.commit()

    # Обновляем данные пользователя
    await session.refresh(user)

    return ex
@app.delete('/remove/user/extensions/{extension_id}')
async def remove_extension_from_user(extension_id: int, user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 
    ex = await session.scalar(select(Extension).where(Extension.id == extension_id))
	
    user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.extensions)))
    
    if not ex:
        raise HTTPException(status_code=404, detail="extension not found")
    if ex in user.extensions:
        user.extensions.remove(ex)
    await session.commit()
    await session.refresh(user)

    return True



@app.get('/by-id', response_model=ShowExtension)
async def get_extension_by_id(extension_id: int, session:AsyncSession = Depends(get_session)): 
	extension = await session.scalar(select(Extension).where(Extension.id == extension_id))
	if extension:
		return extension
	else:
		raise HTTPException(detail={"message":"extension is not exist", "status_code":404}, status_code=404)




	