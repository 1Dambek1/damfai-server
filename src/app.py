import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# routers
from .achievements.achievements_router import app as achievements_app
from .app_auth.auth_router import app as auth_app
from .books.books_router import app as books_app
from .bookmarks.bookmarks_router import app as bookmarks_app
from .analytics.analytics_router import app as analytic_app
from .ai_app.gigachat_router import app as gigachat_app
from .books_to_reading.booksRead_router import app as books_read_app
from .utils.utils_router import app as utils_app
app = FastAPI(title="damfai")


# routers 

app.include_router(auth_app)
app.include_router(books_app)
app.include_router(bookmarks_app)
app.include_router(analytic_app)
app.include_router(gigachat_app)
app.include_router(books_read_app)
app.include_router(achievements_app)
app.include_router(utils_app)


if not os.path.exists("images"):
    os.mkdir("images")

if not os.path.exists("images/books_img"):
    os.mkdir("images/books_img")

if not os.path.exists("audios"):
    os.mkdir("audios")

if not os.path.exists("audios/books"):
    os.mkdir("audios/books")


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




# __________________________________DB(DEBUG)__________________________________


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

