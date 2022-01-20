# Задача 2. Сложить собранные новости из первого задания в БД.
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from task_1_hw_4 import collecting_news
from pprint import pprint

IP_ADDRESS = '127.0.0.1'
PORT = 27017

client = MongoClient(IP_ADDRESS, PORT)
db = client['news_parsing_database']
news_mail = db.news_mail

count_new_news, duplicate_news = 0, 0

for news in collecting_news():
    try:
        news_mail.insert_one(news)
        count_new_news += 1
        # print('НОВОСТЬ ЗАПИСАНА В БД')
    except DuplicateKeyError:
        # print('новость уже в бд')
        duplicate_news += 1
        pass

print(f'В базу данных добавлено - {count_new_news} новостей, дубликаты - {duplicate_news} штук')

for doc in news_mail.find({}):
    pprint(doc, sort_dicts=False)
