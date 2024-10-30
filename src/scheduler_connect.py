# scheduler
import asyncio

import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from .db import session as connect
from .running.running_models import  Prize, Winner, Status
from .app_auth.auth_models import User
from .running.running_utils import get_active_running


async def finish_running_task():
    async with connect() as session:
        running = await get_active_running(session=session)
        
        if running:
            current_date =datetime.datetime.now(datetime.timezone.utc)
            current_date = current_date.astimezone(datetime.timezone.utc).replace(tzinfo=None)
            if running.end_running_date <= current_date:
                running.status = Status.finished
                
                ranked_users = (
                        select(
                            User.id,
                            User.name,
                            User.surname,
                            User.running_points,
                            func.row_number().over(order_by=User.running_points.desc()).label("ranking")
                        )
                        .order_by(User.running_points.desc())
                        .limit(10)
                    )
                result = await session.execute(ranked_users)
                
                data =  [
                    {
                        "id": user_id,
                        "name": name,
                        "surname": surname,
                        "running_points": running_points,
                        "rank": ranking
                    }
                    for user_id, name, surname, running_points, ranking in result
                ]
                
                for user in data:
                    prize = await session.scalar(select(Prize).where(Prize.place == user["rank"], Prize.running_id == running.id))
                    if prize:
                        user = await session.scalar(select(User).where(User.id == user["id"]))
                        user.balance += prize.chappi_tokens
                        user.running_points = 0
                        winner = Winner(user_id=user.id, prize_id=prize.id, running_id=running.id)
                        session.add(winner)
                await session.commit()
                    
                return True
    return False


async def cancel_running_task():
    while True:
        result = await finish_running_task()
        if result:
            break
        await asyncio.sleep(60*60*2) # should fix on celery 
        
