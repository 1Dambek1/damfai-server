from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,text
from sqlalchemy.orm import selectinload

import datetime

from .running_models import Running, Status

from ..config import config
from ..db import session



async def get_active_running(session:AsyncSession):
    running = await session.scalar(select(Running).where(Running.status == Status.started))
    if running:
        return running
    return None





async def update_running_status():
    async with session() as session:
        running = await session.scalar(select(Running).where(Running.status == Status.started))
        if running :
            if running.start_running_date <= datetime.date.today() <= running.end_running_date:
                running.status = Status.finished
                await session.commit()
                return True
