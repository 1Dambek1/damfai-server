import json
import logging
import pathlib
from fastapi import APIRouter, Depends, HTTPException
from ..config  import config
from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session

from .ranks_models import Rank

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload




app = APIRouter(prefix="/ranks", tags=["ranks"])


@app.get('/all')
async def get_all_ranks(session:AsyncSession = Depends(get_session)):    
	ranks = await session.scalars(select(Rank))
	return ranks

@app.post('/create/all')
async def create_all_ranks(session:AsyncSession = Depends(get_session)): 
	BASE_DIR  = pathlib.Path(__file__)
	ranks_data_url = f"{BASE_DIR}app/ranks.json"
	logging.error(ranks_data_url)
	with open(ranks_data_url, "r", encoding='utf-8') as f:
		ranks = json.load(f)
	for i in ranks:
		rank = Rank(name=i["name"], description=i["description"])
		session.add(rank)

	await session.commit()

	return True


@app.get('{rank_id}')
async def create_all_ranks(rank_id: int, session:AsyncSession = Depends(get_session)): 
	rank = await session.scalar(select(Rank).where(Rank.id == rank_id))
	if rank:
		return rank
	else:
		raise HTTPException(detail={"detail":"Rank is not exist", "status_code":404}, status_code=404)




	