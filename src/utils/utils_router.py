
import datetime
import json
import os
import pathlib

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import Base, engine, get_session
from ..books.books_models import Book, Ganre, Chapter, PageModel


app = APIRouter(prefix="/utils", tags=["utils"])

async def create_db():
    
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except:
            pass
        await  conn.run_sync(Base.metadata.create_all)

        
@app.get("/create_db")
async def db():
    await create_db()
    return True

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

@app.get("/parse/ganres")
async def parse_ganres(session:AsyncSession = Depends(get_session)):
    for i in ganres:
        ganre = Ganre(ganre=i)
        session.add(ganre)
    await session.commit()
    return True




@app.get("/parse/books")
async def parse_books(session:AsyncSession = Depends(get_session)):
    BASE_DIR  = pathlib.Path(__file__).parent.parent.parent.parent
    num = 0
    with open(f"{BASE_DIR}app/parse/data.json", "r", encoding='utf-8') as f:

        data = json.load(f)
        for i in data:
            book = Book(title=i["title"], author=i["author"], desc=i["desc"], age_of_book=i["age_of_book"], writen_date = datetime.date(1985, 7, 19))
            for i2 in i["ganre_id"]:
                ganre = await session.scalar(select(Ganre).where(Ganre.id == int(i2)))
                book.ganres.append(ganre)
            session.add(book)
            await session.flush()
            num = 0
            for i2 in i["chapters"]:
                chapter = Chapter(title=i2["title"], numberOfChapter=i2["numberOfChapter"], book_id = book.id)
                session.add(chapter)
                await session.flush()
                for i3 in i2["pages"]:
                    num += 1
                    page = PageModel(numberOfPage=num, text=i3, chapter_id = chapter.id)
                    session.add(page)
                    await session.flush()
        await session.commit()                



        await session.commit()
        return True