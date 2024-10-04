import json
import os
import pathlib
import random
import select
from fastapi import FastAPI, Depends, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .db  import get_session

from .db import Base, engine

from .books.books_models import Book, Ganre, Chapter, PageModel

from .app_auth.auth_router import app as auth_app
from .books.books_router import app as books_app
from .bookmarks.bookmarks_router import app as bookmarks_app
from .profile.profile_router import app as profile_app
from .ai_app.gigachat_router import app as gigachat_app

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





html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/gigachat/ws/generate_questions/1");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


ganres = ["Роман",
          "Мистика",
          "Детективы и триллеры",
          "Социально-психологический",
          "Любовные романы",
          "Драма и трагедия",
          "Сатира",
          "Проза",
          "Эпистолярный роман",
          "Сказки и легенды",
          "Исторический роман",
          "Новелла",
          "Ужасы",
          "Приключенческие",
          "Русская класика",
          "Поэзия",
          "Роман в письмах",
          "Философия",

          ]

@app.get("/ganres")
async def parse(session:AsyncSession = Depends(get_session)):
    for i in ganres:
        ganre = Ganre(ganre=i)
        session.add(ganre)
    await session.commit()
    return True
@app.get("/parse_book")
async def parse(session:AsyncSession = Depends(get_session)):
    BASE_DIR  = pathlib.Path(__file__).parent.parent.parent
    with open(f"{BASE_DIR}app/parse/data.json", "r", encoding='utf-8') as f:

        data = json.load(f)
        for i in data:
            book = Book(title=i["title"], author=i["author"], desc=i["desc"], age_of_book=i["age_of_book"])
            for i2 in i["ganre_id"]:
                ganre = await session.scalar(select(Ganre).where(Ganre.ganre == i2))
                pass
        return data