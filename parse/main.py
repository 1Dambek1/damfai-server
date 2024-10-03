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
    book = {
      
        'chapters': chapters,
        'age_of_book': random.randint(1, 18),
        # 'writen_date': datetime.datetime.now().time(),
        'desc': '', 
        'author': author,
        'title':title,

    }
    return book
data = [
    generate_book(94, 50),
    generate_book(12, 7),
    generate_book(69, 41),
    generate_book(67, 17),
    generate_book(4207, 5),
    generate_book(64, 46)


]

with open("parse/data.json", "w", encoding='utf-8') as f:
    json.dump(data, f)


