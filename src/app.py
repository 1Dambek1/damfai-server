
import os

from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
# routers
from .app_auth.auth_router import app as auth_app
from .books.books_router import app as books_app
from .bookmarks.bookmarks_router import app as bookmarks_app
from .analytics.analytics_router import app as analytic_app
from .extensions.extensions_router import app as extensions_app
# from .ai_app.gigachat_router import app as gigachat_app
from .reading_books.booksRead_router import app as books_read_app
from .utils.utils_router import app as utils_app
from .themes.themes_router import app as theme_app
from .emotes_books.emotes_books_router import app as emotes_books_app
from .shop.shop_router import app as shop_app
# from .search_book.recommendations_router import app as recommendations_app
from .running.running_router import app as running_app

app = FastAPI(title="damfai")

# routers 
app.include_router(utils_app)

app.include_router(auth_app)

app.include_router(books_app)
app.include_router(bookmarks_app)
app.include_router(books_read_app)
app.include_router(emotes_books_app)
# app.include_router(recommendations_app)

# app.include_router(gigachat_app)

app.include_router(analytic_app)
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


if not os.path.exists("src/images"):
    os.mkdir("src/images")

if not os.path.exists("src/images/books_img"):
    os.mkdir("src/images/books_img")

if not os.path.exists("audios"):
    os.mkdir("audios")

if not os.path.exists("audios/books"):
    os.mkdir("audios/books")
