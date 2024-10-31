from fastapi import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,text
from sqlalchemy.orm import selectinload

import datetime

from .running_models import Running, Status

from ..config import config
from ..db import session



async def get_active_running(session:AsyncSession):
    running = await session.scalar(select(Running).options(selectinload(Running.prizes), selectinload(Running.winners)).where(Running.status == Status.started))
    if running:
        return running
    return None



