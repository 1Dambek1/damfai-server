import datetime
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional

from ...app_auth.auth_models import User, TeacherCard





class TeacherCardFilter(Filter):
    experience__lte: Optional[int] = None
    experience__gte: Optional[int] = None
    time_lesson__lte: Optional[float] = None
    time_lesson__gte: Optional[float] = None
    price_of_lesson__lte: Optional[float] = None
    price_of_lesson__gte: Optional[float] = None
    confirm: Optional[bool] = None

    class Constants(Filter.Constants):
        model = TeacherCard

class TeacherFilter(Filter):
    name__like: Optional[str] = None
    surname__like: Optional[str] = None
    patronymic__like: Optional[str] = None
    
    
    email_confirm: Optional[bool] = None
    
    email__like: Optional[str] = None
    dob__lte: Optional[datetime.date] = None
    dob__gte: Optional[datetime.date] = None
    class Constants(Filter.Constants):
        model = User
