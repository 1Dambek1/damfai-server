from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .running_models import Running, Status

async def get_active_running(session:AsyncSession):
    running = await session.scalar(select(Running).options(selectinload(Running.prizes), selectinload(Running.winners)).where(Running.status == Status.started))
    if running:
        return running
    return None



