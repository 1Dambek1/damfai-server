
import datetime
import json
import pathlib
import asyncio

from fastapi import APIRouter,HTTPException

from random import randint


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.src.running.running_models import Running, Status, Prize
from server.src.running.running_utils import get_active_running
from server.src.themes.themes_models import Theme
from server.src.extensions.extensions_models import Extension
from server.src.books.books_models import Book, Ganre, Chapter, PageModel, Authors, EmoteEnum
from server.src.background_tasks import cancel_running_task


from server.src.db import Base, engine


app = APIRouter(prefix="/utils", tags=["utils"])

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

# create_db
async def create_db():
    
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except:
            pass
        await  conn.run_sync(Base.metadata.create_all)

    # 

# db
# @app.get("/create_db", description="debug")
async def db():
    await create_db()
    return True

# create ganres
# @app.get("/parse/ganres", description="debug")
async def parse_ganres(session:AsyncSession):
    for i in ganres:
        ganre = Ganre(ganre=i)
        session.add(ganre)
    await session.commit()
    return True

# create books
# @app.get("/parse/books", description="debug")
async def parse_books(session:AsyncSession ):
    BASE_DIR  = pathlib.Path(__file__).parent.parent.parent.parent
    num = 0
    with open(f"{BASE_DIR}/parse/new_dataset.json", "r", encoding='utf-8') as f:
        id_img = 0
        data = json.load(f)
        for i in data:
            id_img += 1
            author = await session.scalar(select(Authors).where(Authors.author == i["author"]))
            if not author:    
                author = Authors(author=i["author"])
                session.add(author)
                await session.flush()
            

            emotes = [emote.value for emote in EmoteEnum]
            book = Book(zip_text = i["zip_text"],
                        title=i["title"],
                        author=author.author,
                        desc=i["desc"],
                        age_of_book=i["age_of_book"],
                        writen_date = datetime.date(1985, 7, 19),
                        emote=emotes[randint(0, len(emotes)-1)],
                        file_path = f"{id_img}.jpg"
                        )
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

# create themes
# @app.post('/create/all')
async def create_themes(session:AsyncSession): 
	BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
	themes_data_url = BASE_DIR / 'data' / 'themes.json'
	
	with open(themes_data_url, "r", encoding='utf-8') as f:
		themes = json.load(f)	

	objects = [Theme(**i) for i in themes]

	try:
		session.add_all(objects)
		await session.commit()
	except Exception as e:
		await session.rollback()
		raise e

	return True

# create extensions
# @app.post('/create/all', description="debug")
async def create_extensions(session:AsyncSession): 
	BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
	ex_data_url = BASE_DIR / 'data' / 'extensions.json'
	with open(ex_data_url, "r", encoding='utf-8') as f:
		extensions = json.load(f)
	objects = [Extension(**i) for i in extensions]
	try:
		session.add_all(objects)
		await session.commit()
	except Exception as e:
		await session.rollback()
		raise e


	return True

# create current running
# @app.post("/add_running", description="debug")
async def add_running(author:str,days:int,session:AsyncSession):
    running = await get_active_running(session=session)
    if running:
        raise HTTPException(detail={"detail":"You are already have running", "status_code":400}, status_code=400)
    
    author = await session.scalar(select(Authors).where(Authors.author == author))
    if author:
        start_running_date =datetime.datetime.now(datetime.timezone.utc)
        start_running_date = start_running_date.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        
        running = Running(status = Status.started, name_running="gool",start_running_date=start_running_date,end_running_date=start_running_date + datetime.timedelta(days=days))
        running.author = author
        running.author_name = author.author

        
        for i in range(10):
            prize = Prize(place = i+1, chappi_tokens = 1000*(10-i), running_id = running.id)
            running.prizes.append(prize)
        session.add(running)
        await session.commit()
        asyncio.create_task(cancel_running_task())
        return True
