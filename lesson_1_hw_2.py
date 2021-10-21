# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
import requests

keys = ['API_KEY', 'DEMO_KEY', 'es45XhfPEYo3idYIG190b1DxjtSCDeJ6cnaAkHdX']
with open('lesson_1_hw_2.txt', 'w', encoding='utf-8') as file:
    for key in keys:
        response = requests.get(
            f'https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key={key}')
        file.write(f'Используемый ключ ({key}) - ответ сервера ({response})')
        file.write('\n')
