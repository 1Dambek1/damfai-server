import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from langchain.schema import HumanMessage, SystemMessage
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile



from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

from ..books.books_models import Book
from ..get_current_me import get_current_user
from ..db import get_session
from ..GigaChat_connect import model_for_questions , model_for_zip

make_question_about_book_system = 'отправь мне ответ на мой запрос в формате python словаря , для примера возьми этот словарь с 2 вопросами >>> [{"question": "Что такое книга?","options": {"a":"Это книга о чем-то еще","b":"Это книга о чем-то еще","c":"Книга о чем-то еще","d":"Книга о чем-то еще",},"answer": "a"},{"question": "Что такое слово?","options": {"a":"Это буква","b":"Это буквы","c":"Книга о чем-то еще","d":"Это много був связанных по смыслу",},"answer": "d"}]' 


app = APIRouter(prefix="/gigachat", tags=["gigachat"])


@app.get("/zip_small_text")
async def zip_small_text(text:str,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    context = [SystemMessage(content="Сожми  текст, чтобы он стал меньше в {times} раз"), HumanMessage(content=text)]
    result = model_for_zip.invoke(context)
    return result.content

@app.get("/ask_question")
async def ask_question(question:str,id_book:int,me = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    book = await session.scalar(select(Book).where(Book.id == id_book))
    if book:
        context = [SystemMessage(f"Дай ответ на следующий вопрос обращаясь только к книге '{book.title}' автора '{book.author}'"), HumanMessage(content=question)]
        result = model_for_questions.invoke(context)
        return result.content
    else:
        raise HTTPException(status_code=400, detail={
                "data":"book is not exist",
                "status":400
        })
    

@app.websocket("/ws/ask_question/{book_id}")
async def ask_question_ws(book_id:int,websocket: WebSocket,session:AsyncSession = Depends(get_session)):
    await websocket.accept()
    book = await session.scalar(select(Book).where(Book.id == book_id))
    if book:
        context = [SystemMessage(f"Дай ответ на следующий вопрос обращаясь только к книге '{book.title}' автора '{book.author}'")]
    else:
        raise HTTPException(status_code=400, detail={
                "data":"book is not exist",
                "status":400})
    while True:
        try:
            while True:

                data = await WebSocket.receive_text()
                context.append(HumanMessage(content=data))                 
                result = model_for_questions.invoke(context)
                await websocket.send_text(result.content)
                context.pop(-1)
                context.append(SystemMessage(content=f"последний ответ был: '{result.content}'"))

        except:
            await websocket.close()