
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from typing import  TYPE_CHECKING

from ..db import Base
if TYPE_CHECKING:
    from ..app_auth.auth_models import User

    
class Extension(Base):
  __tablename__ = "extension_table"
  
  id: Mapped[int] = mapped_column(primary_key=True)

  title: Mapped[str]
  description: Mapped[str]    
  slug: Mapped[str]
  
  users: Mapped[list["User"]] = relationship(
        back_populates="extensions",  
        uselist=True,
        secondary="extension_user_table"  
    )
  


class ExtensionUser(Base):
    
    __tablename__ = "extension_user_table"

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    extension_id:Mapped[int] = mapped_column(ForeignKey("extension_table.id"), primary_key=True)
    
