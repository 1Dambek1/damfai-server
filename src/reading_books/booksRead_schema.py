import datetime
from pydantic import BaseModel

class ShowReadingBook(BaseModel):
    book_id:int
    title:str
    author:str
    writen_date:datetime.date
    progress:float