import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr , field_validator




class ShowBookmark(BaseModel):

    id: int
    title: str
    author: str
    desc: str
    writen_date: datetime.date
    age_of_book: int 

    id_current_chapter: int
    current_page: int  


class ShowFavourite(BaseModel):

  id:int
  title: str
  author: str
  desc: str
  writen_date: datetime.date
  age_of_book: int