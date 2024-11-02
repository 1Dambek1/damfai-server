import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

import enum
import typing

from server.src.db import Base

if typing.TYPE_CHECKING:
  from server.src.app_auth.auth_models import User
  from server.src.books.books_models import  Authors
  
class Status(enum.Enum):
    not_started = "not_started"
    started = "started"
    finished = "finished"
  
class Running(Base):
  __tablename__ = "running_table"
  id: Mapped[int] = mapped_column(primary_key=True)
  
  name_running: Mapped[str]
  
  author_name:Mapped[str] = mapped_column(ForeignKey("authors_table.author", ondelete="CASCADE"))
  author:Mapped["Authors"] = relationship(uselist=False)
  
  start_running_date:Mapped[datetime.datetime]
  end_running_date:Mapped[datetime.datetime]
  
  status:Mapped[Status] = mapped_column(default=Status.not_started)
  
  winners:Mapped[list["Winner"]] = relationship(back_populates="running", uselist=True)
  
  prizes:Mapped[list["Prize"]] = relationship(back_populates="running", uselist=True)

class Prize(Base):
  __tablename__ = "prize_table"
  id: Mapped[int] = mapped_column(primary_key=True)
  
  place:Mapped[int]
  
  chappi_tokens:Mapped[int]  
  
  running:Mapped["Running"] = relationship(back_populates="prizes", uselist=False)
  running_id:Mapped[int] = mapped_column(ForeignKey("running_table.id", ondelete="CASCADE"))

class Winner(Base):
  __tablename__ = "winners_table"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  
  
  prize_id:Mapped[int] = mapped_column(ForeignKey("prize_table.id", ondelete="CASCADE"), unique=True)
  prize:Mapped["Prize"] = relationship(uselist=False)
  
  running_id:Mapped[int] = mapped_column(ForeignKey("running_table.id", ondelete="CASCADE"))
  running:Mapped["Running"] = relationship(uselist=False)
  
  user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
  user:Mapped["User"] = relationship(uselist=False)