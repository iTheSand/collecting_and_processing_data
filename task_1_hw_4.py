# Задача 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
from pprint import pprint

from lxml import html
import requests
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

response = requests.get('https://news.mail.ru/', headers=header)

dom = html.fromstring(response.text)

url_main_news = dom.xpath(
    "//div//td[contains(@class,'daynews')]//@href | //div/ul[contains(@class,'list_half js-')]/li[@class='list__item']//@href")


def collecting_news():
    news = []
    for url in url_main_news:
        content_article = {}
        response_article_url = requests.get(url, headers=header)
        dom_article_url = html.fromstring(response_article_url.text)
        required_data = dom_article_url.xpath(
            "//div//span[contains(@class,'s__text js-ago')]/@datetime | "
            "//div//span[@class='note']/a/@href | "
            "//div//h1[@class='hdr__inner']/text()")

        content_article['_id'] = int(re.findall(r'\d+', url)[0])
        content_article['название источника'] = required_data[1]
        content_article['наименование новости'] = required_data[2]
        content_article['ссылку на новость'] = url
        content_article['дата публикации'] = required_data[0]
        news.append(content_article)

    return news


if __name__ == '__main__':
    collecting_news()
