import datetime
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional

from ...app_auth.auth_models import User

class StudentFilter(Filter):
    
    name__like: Optional[str] = None
    surname__like: Optional[str] = None
    patronymic__like: Optional[str] = None
    
    
    email_confirm: Optional[bool] = None
    
    email__like: Optional[str] = None
    dob__lte: Optional[datetime.date] = None
    dob__gte: Optional[datetime.date] = None
    
    

    class Constants(Filter.Constants):
        model = User