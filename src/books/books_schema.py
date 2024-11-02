from pydantic import BaseModel


class ShowGanres(BaseModel):
    id: int
    ganre: str 

class CreateRating(BaseModel):
    
    book_id: int
    rating: int

class ShowChapter(BaseModel):
    
    id: int
    title: str | None
    numberOfChapter: int
    pages: int |  None 
    lastNumberOfPage: int |  None

class ShowBookWithChapters(BaseModel):
    
    id: int
    title: str
    author: str

    chapters: list[ShowChapter] |  None

class ShowPage(BaseModel):
    
    numberOfPage: int
    text: str