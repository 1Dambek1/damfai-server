import requests
from bs4 import BeautifulSoup
import datetime
import random
import json
class Ganre:
    id:int
    ganre:str 


class Page:
    
    numberOfPage:int
    text:str


class Chapter:
    
    title:str
    numberOfChapter:int
    pages:list[Page]  

class Book:
    
    title:str
    author:str
    desc: str
    writen_date: datetime.time
    age_of_book: int

    chapters: list[Chapter]
    ganres: list[str]





    

def generate_book(book_id: int, pages_count: int):
    server = requests.get(f"https://ilibrary.ru/text/{book_id}/p.1/index.html")
    soup = BeautifulSoup(server.text)
    chapters = []


    j = 0
    for i in range(1, pages_count+1):
        serv = requests.get(f"https://ilibrary.ru/text/{book_id}/p.{i}/index.html")
        soup2 = BeautifulSoup(serv.text)
        chapter_title = soup2.find('h2')
        # if chapter title is not none append to chapters empty chapter
        if chapter_title:
            j += 1
            chapters.append({
                'title': chapter_title.get_text(),
                'pages': [],
                'numberOfChapter': j
            })
        # page = chapter_title.find_next_sibling('div', {'id': 'pmt1'}).find('pmm')
        ex = []
        _ = soup2.findAll('z')
        for i in _:
            ex.append(i.get_text())
        page = ''.join(ex)

        chapters[-1]['pages'].append(page)
        
        


    author = soup.find('div', {'class': 'author'}).get_text()
    title = soup.find('h1').get_text()
    print(title)
    ganre_id  = [1,2,3,5,8,10,16,18]
    book = {
        'desc': '', 
        'author': author,
        'title':title,
        "ganre_id":ganre_id,
        'chapters': chapters,
        'age_of_book': random.randint(1, 18)
    }
    print("_"*10)

    return book
data = [
    # generate_book(94, 50),
    # generate_book(12, 7),
    # generate_book(69, 41),
    # generate_book(67, 17),
    # generate_book(4207, 5),
    # generate_book(64, 46),
    # generate_book(475, 46),
    # generate_book(1310, 27),
    # generate_book(1334,45),
    # generate_book(107, 15),
    # generate_book(479, 19),
    generate_book(480, 7),
    generate_book(973, 4),
    generate_book(479, 19),
    generate_book(472, 4),
    generate_book(1022, 13),
    # generate_book(1180, 14),
    # generate_book(1545, 6),
    # generate_book(1201, 23),
    # generate_book(1762,6),
    # generate_book(1336, 38),
    # generate_book(1023, 12),
    # generate_book(1484, 9),
    # generate_book(1150, 3),
    # generate_book(1006, 25),
    # generate_book(7, 12),
    # generate_book(1009, 28),
    # generate_book(8, 8),
    # generate_book(1088, 47),
    # generate_book(1070, 22),
    # generate_book(1647, 46),
    # generate_book(1198, 13),
    # generate_book(475, 46),
    # generate_book(67,17 ),
    # generate_book(12, 7),
    # generate_book(107, 15),
    # generate_book(1310, 27),
    # generate_book(1334,45),
]
with open("parse/dataset.json", "w", encoding='utf-8') as f2:
    json.dump(data, f2)
    
    
    
from langchain.chat_models.gigachat import GigaChat
from sentence_transformers import SentenceTransformer

model_for_zip = GigaChat(credentials="NGViMzk4ZGMtNTdhYS00MWU1LTkzM2MtMDlmMGE0NmMyODZkOjFmNDRlMDQyLTI1MDUtNGViZi1hZGVlLWYwZWM2MzgyOGM2MA==", verify_ssl_certs=False, scope="GIGACHAT_API_PERS", streaming=True, model="GigaChat" )
model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')

new_data = []

for i in data:
    text  = (model_for_zip.invoke(f"перескажи за 400 слов все произведение '{i["title"]}' писателя {i["author"]}  не должно быть более 400 слов ")).content

    i["zip_text"] = text
    print(i["title"],i['author'])
    new_data.append(i)
    
with open("parse/new_dataset.json", "w", encoding='utf-8') as f2:
    json.dump(new_data, f2)



