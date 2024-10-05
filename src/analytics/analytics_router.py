import shutil
from typing import Optional
import os 

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.logger import logger

from fastapi_pagination import  add_pagination,Page,paginate
from fastapi_pagination.utils import disable_installed_extensions_check
disable_installed_extensions_check()

from fastapi_filter import FilterDepends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload, aliased
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError

from ..get_current_me import get_current_user
from ..db import get_session

from .analytics_models import PagesPerDay, MinutesPerDay

app = APIRouter(prefix="/analytics", tags=["analytics"])


