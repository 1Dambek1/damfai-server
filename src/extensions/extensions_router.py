
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.get_current_me import get_current_id
from src.db import get_session
from src.app_auth.auth_models import User

from .extensions_models import Extension
from .extensions_schema import  ShowExtension

app = APIRouter(prefix="/extensions", tags=["extensions"])

# get all extensions
@app.get('/all', response_model=list[ShowExtension])
async def get_extensions(session:AsyncSession = Depends(get_session)):    
	extensions = await session.scalars(select(Extension))
	return extensions.all()

# get user extensions
@app.get('/user/extensions', response_model=list[ShowExtension])
async def get_extensions_by_user(user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)): 
	user = await session.scalar(select(User).where(User.id == user_id).options(selectinload(User.extensions)))
	return user.extensions

# get ext by slug
@app.get('/by-slug')
async def get_extension_by_slug(slug: str, session:AsyncSession = Depends(get_session)): 
	extension = await session.scalar(select(Extension).where(Extension.slug == slug))
	if extension:
		return extension
	else:
		raise HTTPException(detail={"message":"extension is not exist", "status_code":404}, status_code=404)

# get ext by id
@app.get('/by-id', response_model=ShowExtension)
async def get_extension_by_id(extension_id: int, session:AsyncSession = Depends(get_session)): 
	extension = await session.scalar(select(Extension).where(Extension.id == extension_id))
	if extension:
		return extension
	else:
		raise HTTPException(detail={"message":"extension is not exist", "status_code":404}, status_code=404)




	