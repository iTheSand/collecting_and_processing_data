# Задача 1. Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(30)
actions = ActionChains(driver)

url_mailbox = 'https://mail.ru/'
driver.get(url_mailbox)

elem = driver.find_element(By.NAME, 'login')
elem.send_keys('study.ai_172')

button = driver.find_element(By.XPATH, '//button[@class="button svelte-1da0ifw"]')
button.click()

elem = driver.find_element(By.NAME, 'password')
elem.send_keys('NextPassword172#')

button = driver.find_element(By.XPATH, '//button[@class="second-button svelte-1da0ifw"]')
button.click()

button = driver.find_element(By.XPATH, '//span[@title="Выделить все"]')
button.click()

sleep(1)
elem = \
    driver.find_element(By.XPATH,
                        '//span[contains(@class,"button2_select-all")]//span[@class="button2__txt"]')

total_number_emails = int(elem.text)
actions.send_keys(Keys.ESCAPE).perform()
print(total_number_emails)

count = 0
url_article_list = []
while count < total_number_emails:
    actions.send_keys(Keys.DOWN).perform()
    sleep(0.05)
    count += 1
    if not count % 15:
        url_mails = driver.find_elements(By.XPATH, '//a[contains(@class,"llc llc_normal")]')
        for i in url_mails:
            url_article_list.append(i.get_attribute('href'))

url_article_set = set(url_article_list)

IP_ADDRESS = '127.0.0.1'
PORT = 27017

client = MongoClient(IP_ADDRESS, PORT)
db = client['mail_parsing_database']
parsing_mail = db.parsing_mail

count_new_mail = 0

for url_article in url_article_set:
    driver.get(url_article)

    try:
        id_mail = int(re.findall(r':\d+:', url_article)[0][1:-2])
        sender = driver.find_element(By.XPATH, '//div[@class="letter__author"]/span').text
        departure_date = driver.find_element(By.XPATH,
                                             '//div[@class="letter__author"]/div[@class="letter__date"]').text
        topic_mail = driver.find_element(By.XPATH, '//h2[@class="thread-subject"]').text
        text_mail = driver.find_element(By.XPATH, '//div[@class="letter-body"]').text

        parsing_mail.insert_one({
            '_id': id_mail,
            'sender': sender,
            'departure_date': departure_date,
            'topic_mail': topic_mail,
            'text_mail': text_mail,
        })
        count_new_mail += 1
    except (NoSuchElementException, DuplicateKeyError) as e:
        print(e)
        pass

for doc in parsing_mail.find({}):
    pprint(doc, sort_dicts=False)

print(f'В базу данных добавлено - {count_new_mail} писем, общее кол-во - {total_number_emails} штук')
