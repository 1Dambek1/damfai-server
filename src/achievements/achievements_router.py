import json
import pathlib
from fastapi import APIRouter, Depends, HTTPException
from ..db import get_session

from .achievements_models import Achievement

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select




app = APIRouter(prefix="/achievements", tags=["achievements"])


@app.get('/all')
async def get_achievements(session:AsyncSession = Depends(get_session)):    
	achievements = await session.scalars(select(Achievement))
	return achievements.all()

@app.post('/create/all')
async def create_achievements(session:AsyncSession = Depends(get_session)): 
	BASE_DIR = pathlib.Path(__file__).resolve().parent.parent .parent
	achievements_data_url = BASE_DIR / 'data' / 'achievements.json'
	with open(achievements_data_url, "r", encoding='utf-8') as f:
		achievements = json.load(f)
	for i in achievements:
		achievement = Achievement(name=i["name"], description=i["description"])
		session.add(achievement)

	await session.commit()

	return True


@app.get('/{achievement_id}')
async def create_all_achievements(achievement_id: int, session:AsyncSession = Depends(get_session)): 
	achievement = await session.scalar(select(Achievement).where(Achievement.id == achievement_id))
	if achievement:
		return achievement
	else:
		raise HTTPException(detail={"detail":"achievement is not exist", "status_code":404}, status_code=404)




	