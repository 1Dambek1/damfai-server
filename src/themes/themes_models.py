


from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from typing import  TYPE_CHECKING
from ..db import Base
if TYPE_CHECKING:
    from ..app_auth.auth_models import User


class Theme(Base):
  __tablename__ = "theme_table"
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] 
  description: Mapped[str]
  backgroundColor: Mapped[str] 
  textColor: Mapped[str] 
  primaryColor: Mapped[str] 
  primaryTextColor: Mapped[str]
  price: Mapped[float] = mapped_column(nullable=True, default=True)

  users: Mapped[list["User"]] = relationship(
        back_populates="themes",  # Указываем обратную связь
        uselist=True,
        secondary="theme_user_table"  # Имя промежуточной таблицы
    )
  


class ThemeUser(Base):
    
    __tablename__ = "theme_user_table"

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    theme_id:Mapped[int] = mapped_column(ForeignKey("theme_table.id"), primary_key=True)
    
