# Задание 2. Написать функцию, которая производит поиск и выводит на экран
# вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
from pymongo import MongoClient
from pprint import pprint

IP_ADDRESS = '127.0.0.1'
PORT = 27017

client = MongoClient(IP_ADDRESS, PORT)
db = client['hh_parsing_database']
python_jun = db.python_jun


def print_salary_vacancies():
    while True:
        print('Введите зарплату, по которой будет осуществлен')
        salary = input('поиск подходящих вакансий в базе данных: ')
        if salary.isdigit():
            salary = int(salary)
            break
        else:
            print('Укажите зп в корректном формате!')

    number_vacancy_found = python_jun.count_documents(
        {'$or': [{'price_job_min': {'$gte': salary}}, {'price_job_max': {'$gte': salary}}]})
    for doc in python_jun.find({'$or': [{'price_job_min': {'$gte': salary}}, {'price_job_max': {'$gte': salary}}]}):
        pprint(doc, sort_dicts=False)
    return f'По заданной зарплате найдено - {number_vacancy_found} вакансий'


if __name__ == '__main__':
    print(print_salary_vacancies())
