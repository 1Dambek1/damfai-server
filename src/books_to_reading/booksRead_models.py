import datetime
from ..db import Base

from ..books.books_models import Book, PageModel, Rating, Ganre,GanreBook
from ..app_auth.auth_models import User

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey



class Reading_Book(Base):
    
    __tablename__ = "reading_book_table"

    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"), primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)

    book:Mapped["Book"] = relationship(uselist=False)

    last_reading_page:Mapped[int] = mapped_column(default=0)

    is_read:Mapped[bool] = mapped_column(default=False)

    start_to_read:Mapped[datetime.date] = mapped_column(default=datetime.datetime.now().date())

    finish_to_read:Mapped[datetime.date] = mapped_column(nullable=True)