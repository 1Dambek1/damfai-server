import datetime
from pydantic import BaseModel

class ShowBookmark(BaseModel):

    id: int
    title: str
    author: str
    desc: str
    writen_date: datetime.date
    age_of_book: int 

    id_current_chapter: int
    current_page: int  
    current_number_of_page: int


class ShowFavourite(BaseModel):

  id:int
  title: str
  author: str
  desc: str
  writen_date: datetime.date
  age_of_book: int