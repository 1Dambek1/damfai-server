
from fastapi import APIRouter, Depends, HTTPException, WebSocket

from langchain.schema import HumanMessage, SystemMessage

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload,joinedload

from server.src.books.books_models import Book, Chapter, PageModel
from server.src.app_auth.auth_utils.utils import valid_access_token
from server.src.ai_connect import model_for_questions , model_for_zip,model_for_user_questions
from server.src.reading_books.booksRead_models import Reading_Book, ReadingPage
from server.src.get_current_me import get_current_user

from server.src.db import get_session



make_question_about_book_system = 'отправь мне ответ на мой запрос ответ в формате python массива, для примера возьми этот формат , только подставь сюда свои данные >>> [{"question": "Что такое книга?","options": {"a":"Это книга о чем-то еще","b":"Это книга о чем-то еще","c":"Книга о чем-то еще","d":"Книга о чем-то еще",},"answer": "a"},{"question": "Что такое слово?","options": {"a":"Это буква","b":"Это буквы","c":"Книга о чем-то еще","d":"Это много був связанных по смыслу",},"answer": "d"}]' 


app = APIRouter(prefix="/gigachat", tags=["gigachat"])

async def active_model(context, model):
    return model.invoke(context)


# confirm(15 секунд)
@app.get("/zip_small_text")
async def zip_small_text(text:str,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    context = [SystemMessage(content="Сожми  текст, чтобы он стал меньше в {times} раз"), HumanMessage(content=text)]
    result = model_for_zip.invoke(context)
    return result.content

# ask question websocket(12+- секунд)
@app.websocket("/ws/ask_question/{book_id}")
async def ask_question_ws(book_id:int,websocket: WebSocket,session:AsyncSession = Depends(get_session)):
    
    book = await session.scalar(select(Book).where(Book.id == book_id))
    if book:
            context = [SystemMessage(f"Дай ответ на следующий вопрос обращаясь только к книге '{book.title}' автора '{book.author}'")]
    else:
            raise HTTPException(status_code=400, detail={
                    "data":"book is not exist",
                    "status":400})
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            context.append(HumanMessage(content=data)) 
            result = await active_model(context, model=model_for_user_questions)
            await websocket.send_text(str(result.content))
            context = [SystemMessage(f"Дай ответ на следующий вопрос обращаясь только к книге '{book.title}' автора '{book.author}'")]
            context.append(HumanMessage(content=f"последний ответ был: '{result.content}' на вопрос: '{data}'")) 

    except Exception:
        await websocket.close() 

# generate questions(+- 20 секунд)
@app.websocket("/ws/generate_questions/{book_id}")
async def generate_questions(book_id:int , webscoket:WebSocket, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == book_id))
    if book:
        text = f"Создай 2 вопроса о книге /'{book.title}'/ автора /'{book.author}'/ {make_question_about_book_system}"
        context = [SystemMessage(content=text)]
        making_questions = []
        new_text = ""
        if book:
            await webscoket.accept()
            try:
                while True:
                    data = await webscoket.receive_text()

                    for i in range(round(int(data)/2+0.4)):
                        
                        result = ((await active_model(context=context, model=model_for_questions)).content)
                        await webscoket.send_text(result)

                        result = eval(result)

                        making_questions.append(result[0]["question"])
                        making_questions.append(result[1]["question"])
                        
                        new_text = f"{text} Мне нужны вопросы не похожие на эти вопросы : {' ,'.join(making_questions)}"
                        
                        context = [SystemMessage(content=new_text)]
            except Exception:
                await webscoket.close()
    raise HTTPException(detail={"status_code":403, "detail":"You do not read this book"}, status_code=403)
                
# sum all text from book
@app.websocket("/ws/sum_text/book/{book_id}")
async def sum_text(book_id: int, websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    try:
        await websocket.accept()
        token = await websocket.receive_text()
        user_id = await valid_access_token(token=token)
        
        r_book = await session.scalar(
            select(Reading_Book).options(selectinload(Reading_Book.pages))
            .where(Reading_Book.book_id == book_id, Reading_Book.user_id == user_id)
        )
        
        await websocket.send_text(str(user_id))
        
        if r_book:
            last_page = 0
            for text in r_book.pages:
                last_page += 1
                await websocket.send_json({"numberOfPage": text.numberOfPage, "text": text.text})

            while True:
                last_page += 1

                page = await session.scalar(
                    select(PageModel)
                    .join(PageModel.chapter)
                    .join(Chapter.book)
                    .options(joinedload(PageModel.chapter).joinedload(Chapter.book))
                    .where(PageModel.numberOfPage == last_page)
                    .where(Book.id == book_id)  # Перемещено в отдельный where
                )
                if page:
                    # Создаем контекст с более конкретной инструкцией для сжатия
                    context = [
                        SystemMessage(content=f"Выполни функцию сумаризации до максимум 310 слов убрав лишние фразы. Вот текст, который нужно сжать: '{page.text}'")
                    ]

                    result = model_for_zip.invoke(context) 
                    await websocket.send_json({"numberOfPage": last_page, "text": result.content,"chapter_id":page.chapter_id})

                    page_record = ReadingPage(reading_book_id=r_book.id_connect, text=result.content, numberOfPage=last_page, chapter_id=page.chapter_id)
                    session.add(page_record)
                else:
                    await session.commit()
                    await websocket.close()
                    break
        await websocket.close()

    except Exception:
        await session.commit()
        await websocket.close()
