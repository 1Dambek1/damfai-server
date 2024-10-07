from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional

from .books_models import Book

class BookFilter(Filter):
    
    title__like: Optional[str] = None
    author__like: Optional[str] = None


    class Constants(Filter.Constants):
        model = Book