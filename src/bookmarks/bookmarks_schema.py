import datetime
from pydantic import BaseModel

class ShowBookmark(BaseModel):

    id: int
    title: str
    author: str
    desc: str
    writen_date: datetime.date
    age_of_book: int 

    idCurrentChapter: int
    currentPage: int  
    currentNumberOfPage: int

class ShowFavourite(BaseModel):

  id: int
  title: str
  author: str
  desc: str
  writen_date: datetime.date
  age_of_book: int