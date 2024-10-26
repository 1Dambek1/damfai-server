   
import json
import datetime
from typing import Annotated
import uuid
import typing

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from enum import Enum

from ..db import Base

if typing.TYPE_CHECKING:   
    from ..analytics.analytics_models import PagesPerDay, MinutesPerDay
    from ..books.books_models import Book, PageModel
    from ..themes.themes_models import Theme
 

class Role(Enum):
    user = "user"
    admin = "admin"
    
    

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('Europe/Moscow', now())"))]

class UserTg(Base):
    __tablename__ = "user_tg_table"
    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    tg_id:Mapped[int]
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey('user_table.id', ondelete='CASCADE'))
    user:Mapped["User"] = relationship(uselist=False, back_populates="user_tg")

class User(Base):
    
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)    
    user_tg:Mapped[list["UserTg"]] = relationship(uselist=True, back_populates="user")

    role:Mapped[Role] = mapped_column(default=Role.user)

    role:Mapped[Role] = mapped_column(default=Role.user)

    password:Mapped[bytes]
    email:Mapped[str] = mapped_column(unique=True)

    name:Mapped[str]
    surname:Mapped[str]
        
    dob:Mapped[datetime.date]
    
    created_at:Mapped[created_at]

    words_per_minute:Mapped[str] = mapped_column(default=json.dumps([120]))
    words_per_minute:Mapped[str] = mapped_column(default=json.dumps([120]))

    favourite_books:Mapped[list["Book"]] = relationship(back_populates="favourite_for_users", uselist=True, secondary="favourite_user_table")
    bookmarks_on_page:Mapped[list["PageModel"]] = relationship(back_populates="bookmarks_for_user", uselist=True, secondary="bookmark_user_table")
    themes: Mapped[list["Theme"]] = relationship(
        back_populates="users",
        uselist=True,
        secondary="theme_user_table"
    )
    reading_books:Mapped[list["Book"]] = relationship(uselist=True, secondary="reading_book_table")


    pages_per_day:Mapped[list["PagesPerDay"]] = relationship(back_populates="user", uselist=True)
    minutes_per_day:Mapped[list["MinutesPerDay"]] = relationship(back_populates="user", uselist=True)
    
    
    # target_in_books:Mapped[int] = mapped_column(default=0)
    