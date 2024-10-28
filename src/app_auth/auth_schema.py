
import datetime
from pydantic import BaseModel, EmailStr, field_validator

from .auth_models import Role

from ..themes.themes_schema import ShowTheme

class LoginUser(BaseModel):
    
    email: EmailStr
    
    password: str   
    password: str   
    
class RegisterUser(BaseModel):
        
    email: EmailStr
    
    name:str
    surname:str
    
    dob:datetime.date

    password: str | bytes 
    
    @field_validator("password")
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

class ShowUser(BaseModel):
    
    id:int
    role: Role
    role: Role
    name:str
    surname:str
    email: EmailStr
    
    created_at:datetime.datetime
    dob:datetime.date
    themes: list[ShowTheme]

class ShowUserWithToken(BaseModel):
    

    email: EmailStr
    name:str
    surname:str
    
    
    dob:datetime.date

    token:str

class UpdateUser(BaseModel):

    name:str | None
    surname:str | None
    email: EmailStr | None  
    password:str | bytes | None
    
    @field_validator("password")
    def check_password(cls, v):
        if not v:
            return None
        if  len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v