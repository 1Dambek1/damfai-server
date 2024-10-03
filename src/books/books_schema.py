from typing import Optional
from fastapi import File, UploadFile
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
    pages: int | list[ShowPage]  |  None 



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

    chapters:  int | list[ShowChapter] |  None
    ratings: float | list[ShowRating]  |  None
    ganres: list[str] |  None | list[ShowGanres]



class ShowBookWithChapters(BaseModel):
    
    id:int
    title:str
    author:str

    chapters:   list[ShowChapter] |  None

