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

@app.websocket("/zip_text/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = json.loads(await websocket.receive_json())
            make_zip_about_book_system = f"Сажми текст, чтобы прочитать его за {data['time_read']}"
            a = data["text"].split("\n\n")
            for i in a:
                message_context = [SystemMessage(content=make_zip_about_book_system), HumanMessage(content=i)]
            
                result = ((model_for_zip.invoke(message_context)).content)
                await websocket.send_json(json.dumps({"zip":result}))
    except:
        await websocket.close()


@app.websocket("/make_questions")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    message_context = [SystemMessage(content=make_question_about_book_system)]
    try:
        while True:
            data = json.loads(await websocket.receive_json())
            message_context.append(HumanMessage(content=f"Составь только 2 вопросов о книге '{data['title']}' автора '{data['author']}' и дай 4 варианта ответа и только 1 ответ "))
            for i in range(round(data["questions"]/2)):
                result = ((model_for_questions.invoke(message_context)).content)
                while True:
                    try:
                        result = eval(result)
                        await websocket.send_json(json.dumps(result))
                        break
                    except: 
                        continue
    except:
        await websocket.close()


