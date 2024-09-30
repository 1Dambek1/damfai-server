import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class LoginUser(BaseModel):
    
    email: EmailStr
    
    password: str
    
class RegisterUser(BaseModel):
    

    
    
    # ______data_______________________
    
    email: EmailStr
    
    password: str | bytes
    
    
    dob:datetime.date
    
    @field_validator("password")
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

class ShowUser(BaseModel):
    
    id:int
    

    created_at:datetime.datetime
    # ______data_______________________
    
    email: EmailStr
        
    dob:datetime.date



class ShowUserWithToken(BaseModel):
    
    id:int

    # ______data_______________________
    
    email: EmailStr
    token:str
        
    dob:datetime.date



class UpdateUser(BaseModel):
    

    
    
    # ______data_______________________
    
    email: EmailStr    
    
    dob:datetime.date
    
    