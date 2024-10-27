from typing import Optional
from pydantic import BaseModel
import datetime


class ShowGanres(BaseModel):
    id:int
    ganre:str 

class CreateRating(BaseModel):
    
    book_id:int
    rating:int




class ShowChapter(BaseModel):
    
    id:int
    title:Optional[str] = None
    numberOfChapter:int
    pages: int |  None 
    lastNumberOfPage: int |  None

class ShowBookWithChapters(BaseModel):
    
    id:int
    title:str
    author:str

    chapters:   list[ShowChapter] |  None

