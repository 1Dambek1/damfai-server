from os import utime
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
AUTH_KEY_DENIS = "NGViMzk4ZGMtNTdhYS00MWU1LTkzM2MtMDlmMGE0NmMyODZkOjFmNDRlMDQyLTI1MDUtNGViZi1hZGVlLWYwZWM2MzgyOGM2MA=="
AUTH_KEY_KIRIL = "YmM3ZDBjYjAtMGQzZC00NDhhLTk5NTEtN2Q2NjhhYjRiZmU4OjBkNjBlMzNjLWFmZWYtNGFkYy05YTI4LTJjOTI3MGNkZTM1Zg=="
SCOPE  = "GIGACHAT_API_PERS"

model_for_questions = GigaChat(credentials=f'{AUTH_KEY_KIRIL}', verify_ssl_certs=False, scope=f"{SCOPE}", streaming=True, model="GigaChat-Pro" ) 
model_for_user_questions = GigaChat(credentials=f'{AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{SCOPE}", streaming=True, model="GigaChat" )
model_for_zip = GigaChat(credentials=f'{AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{SCOPE}", streaming=True, model="GigaChat" )






