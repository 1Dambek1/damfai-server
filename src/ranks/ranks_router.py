import datetime
import logging
import os
from fastapi import APIRouter, Depends, HTTPException
import shutil
from ..config  import config
import requests
from ..get_current_me import get_current_id, get_current_user
from ..app_auth.auth_models import User
from ..db import get_session
from ..books.books_models import Book, Chapter, PageModel
from ..analytics.analytics_models import PagesPerDay
from fastapi.responses import FileResponse

from .ranks_models import Reading_Book

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload