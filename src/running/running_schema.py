from pydantic import BaseModel
from typing import Annotated
import datetime

from .running_models import Status

from ..app_auth.auth_schema import ShowUser 

class PrizeSchema(BaseModel):
    
    place:int
    chappi_tokens:int

class WinnerSchema(BaseModel):
    
    prize:PrizeSchema
    user: ShowUser
    

class RunningSchema(BaseModel):
    id:int
    name_running: str
    author_name: str
    start_running_date: Annotated[datetime.date, None]
    end_running_date: Annotated[datetime.date, None]

    Status: Status


    winners:list[WinnerSchema] | None
    prizes:list[PrizeSchema] | None


class RankedUser(BaseModel):
    id:int
    name: str
    surname: str
    running_points: int
    rank: int
    
class RankingSchema(BaseModel):
    top_100_users:list[RankedUser]
    your_rank:RankedUser