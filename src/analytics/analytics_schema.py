import datetime
from pydantic import BaseModel

class CommonReadingInfo(BaseModel):

        books_count: int | None
        pages_count: int | None
        words_per_min: int | None
        minutes_per_day: int | None
        pages_per_month: int | None
        books_per_month: int | None


class PerDateData(BaseModel):
        start_date: datetime.date
        end_date: datetime.date
        Monday:int
        Tuesday:int
        Wednesday:int
        Thursday:int
        Friday:int
        Saturday:int
        Sunday: int

class PerMonthData(BaseModel):
        January:int
        February:int
        March:int
        April:int
        May:int
        June:int
        July:int
        August:int
        September:int
        October:int
        November:int
        December:int

#  favourite_janre
# Zip text webscokets
#  system of recommendations