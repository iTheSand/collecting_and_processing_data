import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=3&click_from=facet'
        'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=2&click_from=facet'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//span[contains(text(),'Дальше')]/../../../@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[contains(@class,'-result-item')]//a[contains(@href,'/vakansii/')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='_2Wp8I _3a-0Y _3DjcL _3fXVo']/text()").getall()
        url = response.url

        yield JobparserItem(name=name, salary=salary, url=url)
