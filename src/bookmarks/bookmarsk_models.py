from ..db import Base

from ..books.books_models import Book, PageModel, Rating, Ganre,GanreBook
from ..app_auth.auth_models import User

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class FavouriteUser(Base):
    
    __tablename__ = "favourite_user_table"


    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"),  primary_key=True)
    


class BookmarkUser(Base):
    
    __tablename__ = "bookmark_user_table"

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    page_id:Mapped[int] = mapped_column(ForeignKey("page_table.id"), primary_key=True)
    
