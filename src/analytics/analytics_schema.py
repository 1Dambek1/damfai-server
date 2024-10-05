from pydantic import BaseModel

class CommonReadingInfo(BaseModel):

        books_count: int
        pages_count: int
        words_per_min: int
        minutes_per_day: int
        pages_per_month: int
        books_per_month: int