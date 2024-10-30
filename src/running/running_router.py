
import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .running_models import Running, Status, Winner, Prize
from .running_utils import get_active_running

from ..get_current_me import  get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, Chapter, PageModel, Authors
from ..analytics.analytics_models import PagesPerDay
app = APIRouter(prefix="/running", tags=["running"])


@app.get("/authors")
async def get_authors(session:AsyncSession = Depends(get_session)):
    authors = await session.scalars(select(Authors).options(selectinload(Authors.books)))
    return authors.all()

@app.post("/add_running")
async def add_running(author:str,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    running = await get_active_running(session=session)
    if running:
        raise HTTPException(detail={"detail":"You are already have running", "status_code":400}, status_code=400)
    
    author = await session.scalar(select(Authors).where(Authors.author == author))
    if author:
        
        running = Running(status = Status.started, name_running="gool",start_running_date=datetime.date.today(),end_running_date=datetime.date.today()+ datetime.timedelta(days=1))
        running.author = author
        running.author_name = author.author
        session.add(running)
        await session.commit()
        return True
    
@app.get("/running")
async def get_running(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    running = await get_active_running(session=session)
    if running:
        return running
    raise HTTPException(detail={"detail":"You are not running", "status_code":400}, status_code=400)


@app.delete("/running")
async def delete_running(me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    running = await session.scalars(select(Running))
    if running:
        session.delete(running)
        await session.commit()
        return True