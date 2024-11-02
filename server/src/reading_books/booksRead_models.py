import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from server.src.db import Base

from server.src.books.books_models import Book

class Reading_Book(Base):
    
    __tablename__ = "reading_book_table"
    
    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"), primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    id_connect: Mapped[int] = mapped_column(autoincrement=True,primary_key=True, unique=True)

    book:Mapped["Book"] = relationship(uselist=False)

    last_reading_page:Mapped[int] = mapped_column(default=0)

    is_read:Mapped[bool] = mapped_column(default=False)

    start_to_read:Mapped[datetime.date] = mapped_column(default=datetime.datetime.now().date())

    finish_to_read:Mapped[datetime.date] = mapped_column(nullable=True)

    target_of_date:Mapped[datetime.date] = mapped_column(nullable=True)
    
    pages:Mapped[list["ReadingPage"]] = relationship(uselist=True, back_populates="r_book")
    
class ReadingPage(Base):
    __tablename__ = "reading_page"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Внешний ключ для связи с Reading_Book
    reading_book_id: Mapped[int] = mapped_column(ForeignKey("reading_book_table.id_connect"))
    numberOfPage:Mapped[int]
    text: Mapped[str]
    chapter_id:Mapped[int]
    
    r_book:Mapped["Reading_Book"] = relationship(uselist=False, back_populates="pages")
