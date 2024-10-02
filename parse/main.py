import requests
from bs4 import BeautifulSoup
import datetime


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

def prepare_pages_list():
    pages = []
    for i in range(1, 21):
        server = requests.get(f"https://ilibrary.ru/text/4551/p.{i}/index.html")

        soup = BeautifulSoup(server.text)
        content = soup.find("pmm")
        pages.append(content.get_text())
    return pages

    
data = [
    {
        "pages": prepare_pages_list()
    }
]

print(data)
