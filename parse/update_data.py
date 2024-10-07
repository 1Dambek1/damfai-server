# import json
# from os import utime
# from langchain.schema import HumanMessage, SystemMessage
# from langchain.chat_models.gigachat import GigaChat
# AUTH_KEY_DENIS = "NGViMzk4ZGMtNTdhYS00MWU1LTkzM2MtMDlmMGE0NmMyODZkOjFmNDRlMDQyLTI1MDUtNGViZi1hZGVlLWYwZWM2MzgyOGM2MA=="
# SCOPE  = "GIGACHAT_API_PERS"



# model_for_zip = GigaChat(credentials=f'{AUTH_KEY_DENIS}', verify_ssl_certs=False, scope=f"{SCOPE}", streaming=True, model="GigaChat" )





# result = model_for_zip.invoke("Перескажи все произведение 'Евгений Онегин' от пушкина за 500-510 слов")
# text = result.content
# with open("parse/data.json", "r+", encoding='utf-8') as f:
#     data = json.load(f)
#     new_data = []
#     for i in data:
#         text  = (model_for_zip.invoke(f"перескажи за 500-510 слов все произведение '{i["title"]}' писателя {i["author"]} ")).content
#         print(text)
#         print("_"*20)
#         i["zip_text"] = text
#         new_data.append(i)

#     with open("parse/new_dataset.json", "w", encoding='utf-8') as f2:
#         json.dump(new_data, f2)



import os
import json
from transformers import AutoTokenizer, AutoModel
import torch
from torch import Tensor
import torch.nn.functional as F

# We won't have competing threads in this example app
# os.environ["TOKENIZERS_PARALLELISM"] = "false"


# # # Initialize tokenizer and model for GTE-base
# tokenizer = AutoTokenizer.from_pretrained('thenlper/gte-base')
# model = AutoModel.from_pretrained('thenlper/gte-base')


# def average_pool(last_hidden_states: torch.Tensor, attention_mask: Tensor) -> Tensor:
#     last_hidden = last_hidden_states.masked_fill(
#         ~attention_mask[..., None].bool(), 0.0)
#     return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


# def generate_embeddings(text, metadata={}):
#     combined_text = " ".join(
#         [text] + [v for k, v in metadata.items() if isinstance(v, str)])

#     inputs = tokenizer(combined_text, return_tensors='pt',
#                        max_length=512, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)

#     attention_mask = inputs['attention_mask']
#     embeddings = average_pool(outputs.last_hidden_state, attention_mask)

#     embeddings = F.normalize(embeddings, p=2, dim=1)

#     return json.dumps(embeddings.numpy().tolist()[0])


# with open("parse/new_dataset.json", "r", encoding='utf-8') as f:
#     data = json.load(f)
#     for i in data:
#         print(i["zip_text"])

