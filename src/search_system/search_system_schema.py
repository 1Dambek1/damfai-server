import datetime
from typing import Optional
from pydantic import BaseModel

class ShowRecomendations(BaseModel):
    id: int
    title: str
    author: str
    desc: Optional[str] = None
    writen_date: Optional[datetime.date] = None
    age_of_book: Optional[int] | None
    similarity: float
    ganres: list[str]
    ratings: float

