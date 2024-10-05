import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, logger
from langchain.schema import HumanMessage, SystemMessage
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile



from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

from ..books.books_models import Book
from ..get_current_me import get_current_user
from ..db import get_session
from ..GigaChat_connect import model_for_questions , model_for_zip,model_for_user_questions

make_question_about_book_system = 'отправь мне ответ на мой запрос в формате python словаря , для примера возьми этот словарь с 2 вопросами >>> [{"question": "Что такое книга?","options": {"a":"Это книга о чем-то еще","b":"Это книга о чем-то еще","c":"Книга о чем-то еще","d":"Книга о чем-то еще",},"answer": "a"},{"question": "Что такое слово?","options": {"a":"Это буква","b":"Это буквы","c":"Книга о чем-то еще","d":"Это много був связанных по смыслу",},"answer": "d"}]' 


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

    except Exception as e:
        await websocket.send_text(str(e))
        await websocket.close() 

# generate questions(+- 20 секунд)
@app.websocket("/ws/generate_questions/{book_id}")
async def generate_questions(book_id:int , webscoket:WebSocket, session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == book_id))
    text = f"Создай 2 вопроса о книге '{book.title}' автора '{book.author}' {make_question_about_book_system}"
    context = [SystemMessage(content=text)]
    quest = []
    new_text = ""
    if book:
        await webscoket.accept()
        try:
            while True:
                data = await webscoket.receive_text()


    
                for i in range(round(int(data)/2)):

                    result = ((await active_model(context=context, model=model_for_questions)).content)
                    await webscoket.send_text(result)

                    result = eval(result)

                    quest.append(result[0]["question"])
                    quest.append(result[1]["question"])
                    new_text = f"{text} Не повторяй эти вопросы : {" ,".join(quest)}"
                    context = [SystemMessage(content=new_text)]

        except Exception as e:
            await webscoket.send_text(str(e))   
            await webscoket.close()