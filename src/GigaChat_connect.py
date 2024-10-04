from os import utime
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from .config import config

model_for_questions = GigaChat(credentials=f'{config.gigachat_data.AUTH_KEY_KIRIL}', verify_ssl_certs=False, scope=f"{config.gigachat_data.SCOPE}", streaming=True, model="GigaChat-Pro" ) 
model_for_user_questions = GigaChat(credentials=f'{config.gigachat_data.AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{config.gigachat_data.SCOPE}", streaming=True, model="GigaChat" )
model_for_zip = GigaChat(credentials=f'{config.gigachat_data.AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{config.gigachat_data.SCOPE}", streaming=True, model="GigaChat" )






