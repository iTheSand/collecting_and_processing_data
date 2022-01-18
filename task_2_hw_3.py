# Задание 2. Написать функцию, которая производит поиск и выводит на экран
# вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
from bs4 import BeautifulSoup
import requests
from pprint import pprint


# функция преобразования зарплаты к числу
def str_money_to_int(str_money):
    int_money = int(str_money.replace("\u202f", ""))
    return int_money


# функция для парсинга hh.ru
def job_parsing_by_salary():
    print('Программа для сбора информации по вакансиям с сайта hh.ru.')
    # результирующий список
    result = []
    str_pos = ''

    position = input('Введите интересующую должность: ')
    # приводим вводимую должность к нужному формату
    # пример: python разработчик -> python+разработчик
    for el in position:
        if el == ' ':
            el = '+'
        str_pos += el

    while True:
        print('Введите желаемую зп и валюту, в формате 150000 руб. / 2500 USD: ')
        salary_and_cur = input('- ').split(' ')
        salary = salary_and_cur[0]
        cur = salary_and_cur[1]
        if salary.isdigit() and (cur == 'руб.' or cur == 'USD'):
            salary = int(salary)
            break
        else:
            print('Укажите зп в корректном формате!')

    while True:
        print('Введите корректный диапазон анализируемых страниц,')
        print('от 1-ой до 100-ой страницы включительно')
        quantity_page = int(input('- '))
        if 0 < quantity_page <= 100:
            break
        else:
            print('Указано не корректное кол-во анализируемых страниц!')

    # парсим указанное кол-во страниц сайта
    for page in range(quantity_page):
        # url-адрес запроса к сайту hh.ru,
        # где str_pos - должность в нужном формате, page - кол-во страниц, которые парсим
        url = f'https://hh.ru/search/vacancy?area=113&fromSearchLine=true&text={str_pos}&from=suggest_post&page={page}&items_on_page=20'
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
            # зарплата
            price_job = el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if price_job is None:
                continue
            else:
                lst_job_price = el.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.split(' ')
                currency = lst_job_price[-1]
                if len(lst_job_price) == 3:
                    price_job_min = price_job_max = str_money_to_int(lst_job_price[1])
                else:
                    price_job_min, price_job_max = str_money_to_int(lst_job_price[0]), \
                                                   str_money_to_int(lst_job_price[2])
            if cur != currency:
                continue
            elif price_job_min < salary and price_job_max < salary:
                continue
            else:
                # название должности
                name_job = el.find('span', {'class': 'g-user-content'}).find('a').text
                # ссылка на вакансию
                link = el.find('span', {'class': 'g-user-content'}).find('a').get('href')
                # сайт, который парсим
                # заполняем список полученными данными
                result.append({
                    'name_job': name_job,
                    'price_job_min': price_job_min,
                    'price_job_max': price_job_max,
                    'currency': currency,
                    'link': link
                })
        button_next = soup.find('a', {'data-qa': 'pager-next'})
        if not button_next:
            print(f'{page} - последняя страница')
            break
    return result


if __name__ == '__main__':
    pprint(job_parsing_by_salary(), sort_dicts=False)
