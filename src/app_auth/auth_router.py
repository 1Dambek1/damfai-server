from fastapi import APIRouter, Depends, HTTPException


from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from .auth_schema import RegisterUser, LoginUser, ShowUser, UpdateUser
from .auth_utils.utils import decode_password, check_password, create_access_token


from ..db import get_session
from .auth_models import User
from ..get_current_me import get_current_user



app = APIRouter(prefix="/auth", tags=["auth"])


@app.get("/me", response_model=ShowUser)
async def me(me:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
     return me


@app.post("/login")
async def login_user(data:LoginUser,session:AsyncSession = Depends(get_session)):

    user = await session.scalar(select(User).where(User.email == data.email))

    if user:
        if await check_password(password=data.password, old_password=user.password):
                user_token = await create_access_token(user_id=user.id)
                return {"token":user_token}

    raise HTTPException(status_code=401, detail={
                "data":"user is not exists",
                "status":401
        })
        

@app.post("/register")
async def register_user(data:RegisterUser ,session:AsyncSession = Depends(get_session)):
    data_dict = data.model_dump()
    
    data_dict["password"] = await decode_password(password=data.password)
    
    
    user = User(**data_dict)
    session.add(user) 
    await session.flush()

    user_id = user.id
        
    await session.commit()
        
    user_token = await create_access_token(user_id=user_id)
    data_dict["token"] = user_token  
        
    return data_dict
    


@app.put("/update", response_model=ShowUser)
async def update_user(data:UpdateUser,me:User = Depends(get_current_user) ,session:AsyncSession = Depends(get_session)):
    
    await session.refresh(me)
    me.email = data.email
    me.dob = data.dob
    await session.commit()
    await session.refresh(me)

    return me


@app.put("/update_password", response_model=ShowUser)
async def update_user(password:str,me:User = Depends(get_current_user) ,session:AsyncSession = Depends(get_session)):
    
    await session.refresh(me)
    me.password = await decode_password(password=password)
    await session.commit()
    await session.refresh(me)

    return me
