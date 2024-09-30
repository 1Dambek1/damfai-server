import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr , field_validator
class ShowPage(BaseModel):
    
    id:int

class ShowChapter(BaseModel):
    
    id:int
    title:Optional[str] = None
    numberOfChapter:int


class ShowUserWithBookMarks(BaseModel):
    
    id:int
    
    name:str
    surname:str
    email: EmailStr
    
    created_at:datetime.datetime

    dob:datetime.date

    bookmarks:list[ShowPage] | None

class ShowUserWithFavourite(BaseModel):
    
    id:int
    
    name:str
    surname:str
    email: EmailStr
    
    created_at:datetime.datetime

    dob:datetime.date

    bookmarks:list[ShowChapter] | None
    