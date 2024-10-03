import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine

from .app_auth.auth_router import app as auth_app
from .books.books_router import app as books_app
from .bookmarks.bookmarks_router import app as bookmarks_app
from .profile.profile_router import app as profile_app
from .gigachat_app.gigachat_router import app as gigachat_app

app = FastAPI(title="damfai")

if not os.path.exists("images"):
    os.mkdir("images")

if not os.path.exists("images/books_img"):
    os.mkdir("images/books_img")
# routers 

app.include_router(auth_app)
app.include_router(books_app)
app.include_router(bookmarks_app)
app.include_router(profile_app)
app.include_router(gigachat_app)
# DB(DEBUG)

async def create_db():
    
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except:
            pass
        await  conn.run_sync(Base.metadata.create_all)

        
@app.get("/db")
async def create():
    await create_db()
    return True

# alembic
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

