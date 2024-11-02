
import os
import sys
sys.path.append('/app')

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routers

from .app_auth.auth_router import app as auth_app

from .books.books_router import app as books_app
from .bookmarks.bookmarks_router import app as bookmarks_app
from .reading_books.booksRead_router import app as books_read_app
from .emotes_books.emotes_books_router import app as emotes_books_app

from .analytics.analytics_router import app as analytic_app
from .ai_app.gigachat_router import app as gigachat_app
from .search_system.search_system_router import app as search_system_app
from .second_stage.second_stage_router import app as second_stage_app

from .extensions.extensions_router import app as extensions_app
from .themes.themes_router import app as theme_app
from .shop.shop_router import app as shop_app

from .running.running_router import app as running_app

# routers end


from .utils.utils_router import db, parse_ganres, parse_books, create_themes, create_extensions,add_running
from .db import session

app = FastAPI(title="damfai", version="0.3")

# routers

app.include_router(auth_app)

app.include_router(books_app)
app.include_router(bookmarks_app)
app.include_router(books_read_app)
app.include_router(emotes_books_app)

app.include_router(search_system_app)
app.include_router(gigachat_app)
app.include_router(analytic_app)
app.include_router(second_stage_app)

app.include_router(theme_app)
app.include_router(extensions_app)
app.include_router(shop_app)

app.include_router(running_app)



# CORS

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


# dir

# if not os.path.exists("src/images"):
#     os.mkdir("src/images")

# if not os.path.exists("src/images/books_img"):
#     os.mkdir("src/images/books_img")

if not os.path.exists("audios"):
    os.mkdir("audios")

if not os.path.exists("audios/books"):
    os.mkdir("audios/books")
    

# init project

async def init_db_and_data(session: AsyncSession):
    await db()  # Если db() также требует сессии
    await parse_ganres(session=session)
    await parse_books(session=session)
    await create_themes(session=session)
    await create_extensions(session=session)
    await add_running(session=session, author="Федор Достоевский", days=31)

@app.on_event("startup")
async def startup():
    async with session() as connect: 
        await init_db_and_data(connect)