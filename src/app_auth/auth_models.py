from ..db import Base


import datetime
from typing import Annotated
import uuid
import typing

from sqlalchemy import  text, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:    
    from ..bookmarks.bookmarsk_models import Bookmark, Favourite
    from ..books.books_models import Book, PageModel, Rating, Ganre,GanreBook


created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('Europe/Moscow', now())"))]


class User(Base):
    
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)    

    password:Mapped[bytes]
    email:Mapped[str] = mapped_column(unique=True)

    name:Mapped[str]
    surname:Mapped[str]
        
    dob:Mapped[datetime.date]
    
    created_at:Mapped[created_at]

    books_per_month:Mapped[int] = mapped_column(nullable=True)
    

    favourite:Mapped[list["Book"]] = relationship(uselist = True, secondary="favourite_table", back_populates="favourite_for")
    
    bookmarks:Mapped[list["PageModel"]] = relationship(uselist = True, secondary="bookmark_table", back_populates="bookmark_for")

