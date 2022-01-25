# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            result_salary = self.process_salary_hh(item.get('salary'))
        else:
            result_salary = self.process_salary_sj(item.get('salary'))
        item['salary_min'] = result_salary[0]
        item['salary_max'] = result_salary[1]
        item['currency'] = result_salary[2]
        del item['salary']
        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass

        return item

    def str_money_to_int(self, str_money):
        int_money = int(str_money.replace("\xa0", ""))
        return int_money

    def process_salary_hh(self, salary):
        if len(salary) < 2:
            salary = [None, None, None]
        elif 2 < len(salary) <= 5:
            salary = [self.str_money_to_int(salary[1]), self.str_money_to_int(salary[1]), salary[3]]
        else:
            salary = [self.str_money_to_int(salary[1]), self.str_money_to_int(salary[3]), salary[5]]

        return salary

    def process_salary_sj(self, salary):
        if len(salary) < 2:
            salary = [None, None, None]
            print(salary)
        else:
            salary.remove('\xa0')
            print(salary)
            if salary[0] == 'от' or salary[0] == 'до':
                res_lst = salary[1].split('\xa0')
                money = int(res_lst[0] + res_lst[1])
                cur = res_lst[2]
                salary = [money, money, cur]
                print(salary)
            elif len(salary) >= 3:
                salary = [self.str_money_to_int(salary[0]), self.str_money_to_int(salary[1]), salary[2]]
                print(salary)
            else:
                salary = [self.str_money_to_int(salary[0]), self.str_money_to_int(salary[0]), salary[1]]
                print(salary)

        return salary
