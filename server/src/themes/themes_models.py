
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from server.src.db import Base
if TYPE_CHECKING:
    from server.src.app_auth.auth_models import User


class Theme(Base):
  __tablename__ = "theme_table"
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  description: Mapped[str]
  light: Mapped[dict] = mapped_column(JSON)
  dark: Mapped[dict] = mapped_column(JSON)
  price: Mapped[float] = mapped_column(nullable=True, default=0)
  key:Mapped[str]

  users: Mapped[list["User"]] = relationship(
        back_populates="themes",  
        uselist=True,
        secondary="theme_user_table"  
    )
  
class ThemeUser(Base):
    
    __tablename__ = "theme_user_table"

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    theme_id:Mapped[int] = mapped_column(ForeignKey("theme_table.id"), primary_key=True)
    
