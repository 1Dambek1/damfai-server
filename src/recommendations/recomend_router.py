from fastapi import APIRouter, Depends, HTTPException

from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, Chapter, PageModel
from ..books_to_reading.booksRead_models import Reading_Book
from ..analytics.analytics_models import PagesPerDay, MinutesPerDay

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload, aliased


app = APIRouter(prefix="/recommendations", tags=["recommendations"])


