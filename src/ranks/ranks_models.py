


import datetime
from ..db import Base

from ..books.books_models import Book

from sqlalchemy.orm import Mapped, mapped_column



class Rank(Base):
    
    __tablename__ = "rank_table"
    id:Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str]
    description: Mapped[str]

    

	 