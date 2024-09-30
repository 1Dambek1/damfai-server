from typing import Optional
from pydantic import BaseModel
import datetime

class ShowGanres(BaseModel):
    id:int
    ganre:str 

class ShowRating(BaseModel):
    
    id:int
    book_id:int
    user_id:int 
    rating:int

class CreateRating(BaseModel):
    
    book_id:int
    rating:int

class CreatePage(BaseModel):
    
    numberOfPage:int
    text:str
    chapter_id:int

class ShowPage(BaseModel):
    
    id:int
    numberOfPage:int
    text:str


class CreateChapter(BaseModel):
    
    title:Optional[str] = None
    numberOfChapter:int
    book_id:int

class ShowChapter(BaseModel):
    
    id:int
    title:Optional[str] = None
    numberOfChapter:int
    pages:list[ShowPage] |int |  None 



class CreateBook(BaseModel):
    
    title:str
    author:str
    desc:Optional[str] = None
    writen_date:Optional[datetime.date] = None
    ganres: list[int]
    age_of_book:int

class ShowBook(BaseModel):
    
    id:int
    title:str
    author:str
    desc:Optional[str] = None
    writen_date:Optional[datetime.date] = None
    age_of_book:Optional[int] | None

    chapters:list[ShowChapter] | int |  None
    ratings:list[ShowRating] | float |  None
    ganres: list[str] |  None | list[ShowGanres]




