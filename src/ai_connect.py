
# GIGACHAT

from langchain.chat_models.gigachat import GigaChat
from .config import config

model_for_questions = GigaChat(credentials=f'{config.gigachat_data.AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{config.gigachat_data.SCOPE}", streaming=True, model="GigaChat-Pro" ) 
model_for_user_questions = GigaChat(credentials=f'{config.gigachat_data.AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{config.gigachat_data.SCOPE}", streaming=True, model="GigaChat" )
model_for_zip = GigaChat(credentials=f'{config.gigachat_data.AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{config.gigachat_data.SCOPE}", streaming=True, model="GigaChat" )


# SUM TEXT

from transformers import T5ForConditionalGeneration, T5Tokenizer

device = 'cpu' #or 'cpu' for translate on cpu

model_name = 'utrobinmv/t5_summary_en_ru_zh_base_2048'
model_sum = T5ForConditionalGeneration.from_pretrained(model_name)
model_sum.eval()
tokenizer = T5Tokenizer.from_pretrained(model_name)