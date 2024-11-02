import datetime
from pydantic import BaseModel


class ShowBook(BaseModel):
 
    id: int
    title: str
    author: str
    desc: str | None
    writen_date: datetime.date | None
    age_of_book: int | None
    chapters:  int |  None
    ratings: float |  None
    ganres: list[str] 
    