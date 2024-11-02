import datetime
from pydantic import BaseModel

class ShowReadingBook(BaseModel):
    id: int
    title: str
    author: str
    writen_date: datetime.date
    progress: float
    start_to_read: datetime.date
    finish_to_read: datetime.date | None
    is_read: bool
    
    target_of_date: datetime.date | None