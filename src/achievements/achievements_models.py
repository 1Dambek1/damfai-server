


from ..db import Base

from sqlalchemy.orm import Mapped, mapped_column



class Achievement(Base):
    
    __tablename__ = "achievement_table"
    id:Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str]
    description: Mapped[str]

    

	 