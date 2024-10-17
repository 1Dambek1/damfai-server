


from sqlalchemy.orm import  Mapped, mapped_column, relationship

from ..db import Base


class Theme(Base):
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] 
  description: Mapped[str]
  backgroundColor: Mapped[str] 
  textColor: Mapped[str] 
  primaryColor: Mapped[str] 
  primaryTextColor: Mapped[str]
  price: Mapped[float] = mapped_column(nullable=True, default=True)