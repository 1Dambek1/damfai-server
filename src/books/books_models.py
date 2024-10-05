import datetime
from typing import Annotated, TYPE_CHECKING
import uuid
from sqlalchemy.orm  import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey

from ..db import Base
if TYPE_CHECKING:
    from ..app_auth.auth_models import User


class Rating(Base):
    __tablename__ = "rating_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)

    rating:Mapped[int] = mapped_column(nullable=False)
    
    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"))
    book:Mapped["Book"] = relationship(uselist=False, back_populates="ratings")

    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(uselist=False)


class Book(Base):
    
    __tablename__ = "book_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)

    file_path:Mapped[str] = mapped_column(nullable=True)

    title:Mapped[str]
    author:Mapped[str]
    desc:Mapped[str]
    writen_date:Mapped[datetime.date] = mapped_column(nullable=True)
    age_of_book:Mapped[int] = mapped_column(nullable=True)

    chapters:Mapped[list["Chapter"]] = relationship(back_populates="book", uselist=True)

    ganres:Mapped[list["Ganre"]] = relationship(back_populates="books", uselist=True, secondary="ganre_book_table")

    ratings:Mapped[list["Rating"]] = relationship(back_populates="book", uselist=True)

    favourite_for_users:Mapped[list["User"]] = relationship(back_populates="favourite_books", uselist=True, secondary="favourite_user_table")

    # emabings:Mapped[list[float]] = [1, -10, 12 , 14, 18]


class Chapter(Base):
    
    __tablename__ = "chapter_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)

    title:Mapped[str] = mapped_column(nullable=True)
    numberOfChapter:Mapped[int] = mapped_column()

    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"))
    book:Mapped["Book"] = relationship(uselist=False, back_populates="chapters")

    pages:Mapped[list["PageModel"]] = relationship(back_populates="chapter", uselist=True)

class PageModel(Base):
    
    __tablename__ = "page_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    numberOfPage:Mapped[float] = mapped_column()
    text:Mapped[str]

    chapter_id:Mapped[int] = mapped_column(ForeignKey("chapter_table.id"))
    chapter:Mapped["Chapter"] = relationship(uselist=False, back_populates="pages")

    bookmarks_for_user:Mapped[list["User"]] = relationship(back_populates="bookmarks_on_page", uselist=True, secondary="bookmark_user_table")


class Ganre(Base):  
    __tablename__ = "ganre_table"

    id:Mapped[int] = mapped_column(primary_key=True)
    
    ganre:Mapped[str] 

    books:Mapped[list["Book"]] = relationship(back_populates="ganres", uselist=True, secondary="ganre_book_table")


class GanreBook(Base):  
    __tablename__ = "ganre_book_table"
    
    
    ganre_id:Mapped[int] = mapped_column(ForeignKey("ganre_table.id"), primary_key=True)
    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"), primary_key=True)