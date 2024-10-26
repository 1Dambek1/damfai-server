from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from typing import  TYPE_CHECKING

from ..db import Base
if TYPE_CHECKING:
    from ..app_auth.auth_models import User
    from ..books.books_models import Book
    
    
class Running(Base):
  __tablename__ = "running_table"
  id: Mapped[int] = mapped_column(primary_key=True)
  