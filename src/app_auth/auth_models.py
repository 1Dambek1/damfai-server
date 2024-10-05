from ..db import Base


import datetime
from typing import Annotated
import uuid
import typing

from sqlalchemy import  text, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:    
    from ..bookmarks.bookmarsk_models import BookmarkUser, FavouriteUser
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
    

    favourite_books:Mapped[list["Book"]] = relationship(back_populates="favourite_for_users", uselist=True, secondary="favourite_user_table")

    bookmarks_on_page:Mapped[list["PageModel"]] = relationship(back_populates="bookmarks_for_user", uselist=True, secondary="bookmark_user_table")
    user_tg:Mapped[list["UserTg"]] = relationship(uselist=True, back_populates="user")
	

class UserTg(Base):
    __tablename__ = "user_tg_table"
    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    tg_id:Mapped[int]
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey('user_table.id', ondelete='CASCADE'))
    user:Mapped["User"] = relationship(uselist=False, back_populates="user_tg")