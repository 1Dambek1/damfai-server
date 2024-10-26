import datetime
from typing import Optional
from pydantic import BaseModel



class ShowBook(BaseModel):
 
    id:int
    title:str
    author:str
    desc:Optional[str] = None
    writen_date:Optional[datetime.date] = None
    age_of_book:Optional[int] | None
    chapters:  int |  None
    ratings: float |  None
    ganres: list[str] 
    

