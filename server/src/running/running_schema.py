from pydantic import BaseModel
import datetime

from .running_models import Status

from server.src.app_auth.auth_schema import ShowUser 

class PrizeSchema(BaseModel):
    
    place: int
    chappi_tokens: int

class WinnerSchema(BaseModel):
    
    prize: PrizeSchema
    user: ShowUser
    
class RunningSchema(BaseModel):
    id: int
    name_running: str
    author_name: str
    start_running_date: datetime.datetime | None
    end_running_date: datetime.datetime | None

    status: Status


    winners:list[WinnerSchema] | None
    prizes:list[PrizeSchema] | None

class RankedUser(BaseModel):
    id: int
    name: str
    surname: str
    runningPoints: int
    place: int
    
class RankingSchema(BaseModel):
    topUsers: list[RankedUser]
    userRank: RankedUser