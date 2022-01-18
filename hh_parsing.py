# 1. Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# ### По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
import os
from bs4 import BeautifulSoup
import pandas
import requests
import re


# функция для парсинга hh.ru
def job_parsing():
    print('Программа для сбора информации по вакансиям с сайта hh.ru.')
    # результирующий список
    result = []
    str_pos = ''
    position = input('Введите интересующую должность: ')
    quantity_page = input('Введите кол-во анализируемых страниц: ')
    # приводим вводимую должность к нужному формату
    # пример: python разработчик -> python+разработчик
    for el in position:
        if el == ' ':
            el = '+'
        str_pos += el
    # парсим указанное кол-во страниц сайта
    for page in range(int(quantity_page)):
        # url-адрес запроса к сайту hh.ru,
        # где str_pos - должность в нужном формате, page - кол-во страниц, которые парсим
        url = f'https://hh.ru/search/vacancy?area=113&fromSearchLine=true&text={str_pos}&from=suggest_post&page={page}'
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
            if price_job == None:
                price_job_min = price_job_max = currency = 'None'
            else:
                lst_job_price = el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.split(' ')
                currency = lst_job_price[-1]
                if len(lst_job_price) == 3:
                    price_job_min = price_job_max = lst_job_price[1]
                else:
                    price_job_min, price_job_max = lst_job_price[0], lst_job_price[2]
            # ссылка на вакансию
            link = el.find('span', {'class': 'g-user-content'}).find('a').get('href')
            # сайт, который парсим
            website = f"{re.split('.ru', url)[0]}.ru"
            # заполняем список полученными данными
            result.append({
                'name_job': name_job,
                'price_job_min': price_job_min.replace("\u202f", " "),
                'price_job_max': price_job_max.replace("\u202f", " "),
                'currency': currency,
                'link': link,
                'website': website
            })
    return position, quantity_page, result


# функция записи фрейма данных в excel файл
def record_to_excel():
    data_parsing = job_parsing()
    position = data_parsing[0]
    quantity_page = data_parsing[1]
    name_xlsx_file = f"{os.path.basename(__file__).split('.')[0]}_{position}_{int(quantity_page) * 20}.xlsx"
    df = pandas.DataFrame(data_parsing[2])
    writer = pandas.ExcelWriter(name_xlsx_file)
    df.to_excel(writer, index=False)
    writer.save()
    print(f'Фрейм данных успешно записан в файл {name_xlsx_file}')


if __name__ == '__main__':
    record_to_excel()
