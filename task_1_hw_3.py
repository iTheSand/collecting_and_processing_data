# Задание 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bs4 import BeautifulSoup
from math import inf
import requests
import re

IP_ADDRESS = '127.0.0.1'
PORT = 27017

client = MongoClient(IP_ADDRESS, PORT)
db = client['hh_parsing_database']

MAX_COUNT_PAGE = inf
POSITION = 'python junior'
python_jun = db.python_jun


# функция преобразования зп к числу
def str_money_to_int(str_money):
    int_money = int(str_money.replace("\u202f", ""))
    return int_money


# функция для парсинга hh.ru
def job_parsing_save_db():
    str_pos = ''
    count_page = 0
    count_new_vacancy = 0
    # приводим должность к нужному формату
    # пример: python разработчик -> python+разработчик
    for el in POSITION:
        if el == ' ':
            el = '+'
        str_pos += el
    while True:
        # url-адрес запроса к сайту hh.ru,
        # где str_pos - должность в нужном формате, page - кол-во страниц, которые парсим
        url = f'https://hh.ru/search/vacancy?area=113&fromSearchLine=true&text={str_pos}&from=suggest_post&page={count_page}&items_on_page=20'
        # заголовок обращения, без него сервер не ответит на запрос
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
        # ответ сервера
        response = requests.get(url, headers=headers)
        # парсинг полученного ответа с помощью 'lxml'
        soup = BeautifulSoup(response.text, 'lxml')
        # поиск всех тегов с заданным классом (все карточки вакансий на странице)
        pos = soup.find_all('div', {'class': 'vacancy-serp-item'})
        # перебираем карточки и ищем в каждой нужную инфу
        for el in pos:
            # название должности
            name_job = el.find('span', {'class': 'g-user-content'}).find('a').text
            # зарплата
            price_job = el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if price_job is None:
                price_job_min = price_job_max = currency = None
            else:
                lst_job_price = el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.split(' ')
                currency = lst_job_price[-1]
                if len(lst_job_price) == 3:
                    price_job_min = price_job_max = str_money_to_int(lst_job_price[1])
                else:
                    price_job_min, price_job_max = str_money_to_int(lst_job_price[0]), str_money_to_int(
                        lst_job_price[2])
            # ссылка на вакансию
            link = el.find('span', {'class': 'g-user-content'}).find('a').get('href')
            # уникальный id для базы данных
            id_for_db = int(re.findall(r'\d+', link)[0])
            # сайт, который парсим
            website = f"{re.split('.ru', url)[0]}.ru"
            # заполняем базу данных полученными данными, каждая запись проверяется на уникальность id
            try:
                python_jun.insert_one({
                    '_id': id_for_db,
                    'name_job': name_job,
                    'price_job_min': price_job_min,
                    'price_job_max': price_job_max,
                    'currency': currency,
                    'link': link,
                    'website': website})
                count_new_vacancy += 1
                print('ВАКАНСИЯ ЗАПИСАНА В БД')
            except DuplicateKeyError:
                print('вакансия уже в бд')
                pass
        count_page += 1
        button_next = soup.find('a', {'data-qa': 'pager-next'})
        if not button_next or count_page == MAX_COUNT_PAGE:
            break

    count_doc_in_db = 0
    for doc in python_jun.find():
        count_doc_in_db += 1

    return f'Парсинг {count_page} страниц закончен, ' \
           f'в базу данных добавилось {count_new_vacancy} вакансий, общее кол-во {count_doc_in_db}'


if __name__ == '__main__':
    print(job_parsing_save_db())
