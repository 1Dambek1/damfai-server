import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginUser(BaseModel):
    
    email: EmailStr
    
    password: str
    
class RegisterUser(BaseModel):
    

    
    
    # ______data_______________________
    
    email: EmailStr
    
    password: str | bytes
    
    
    dob:datetime.date
    
    
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



    
    