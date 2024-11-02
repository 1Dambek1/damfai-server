
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .app_auth.auth_utils.utils import valid_access_token
from .db import get_session
from .app_auth.auth_models import Role, User

bearer = HTTPBearer()

async def get_current_id(token:HTTPAuthorizationCredentials = Depends(bearer)):
    
    user_id = await valid_access_token(token=token.credentials)
    
    if not user_id:
        
            raise HTTPException(status_code=426, detail={
                "token":"Your token is not valid",
                "status":426
            })
            
    return user_id



async def get_current_user(user_id = Depends(get_current_id),connection:AsyncSession = Depends(get_session)):
    
    user = await connection.scalar(select(User).options(selectinload(User.themes), selectinload(User.reading_books)).where(User.id == user_id))
    
    if not user:
        
            raise HTTPException(status_code=426, detail={
                "token":"Your token is not valid",
                "status":426
            })

    return user


async def get_current_admin(user = Depends(get_current_user)):
    
    if user.role != Role.admin:
        
            raise HTTPException(status_code=426, detail={
                "token":"You don't have admin rights",
                "status":426
            })

    return user