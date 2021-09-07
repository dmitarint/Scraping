# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
from jobparser.items import JobparserItem


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies1808']

    def Salary_hh(self, item: JobparserItem):
        """"
        Для сайта хэдхантер
        Функция возвращает три переменные - минимальная зп, максимальная зп, валюта
        """
        _salary = item['salary']
        if _salary != 'з/п не указана':
            if 'от ' in _salary and 'до ' not in _salary:  # если у нас только нижняя зп
                _salary = _salary.split(' ')  # делим строку по символу пробел
                print(_salary)
                _mid = _salary[1].split('\xa0')  # берем число и делим по символу пробел
                min_salary = int(''.join(_mid))  # объединяем элементы списка и преобразуем в число
                max_salary = None  # максимальная зп
                curency = _salary[-1]  # тип валюты
            elif 'от ' not in _salary and 'до ' in _salary:  # если у нас только верхняя зп
                _salary = _salary.split(' ')  # делим строку по символу пробел
                _mid = _salary[1].split('\xa0')  # берем число и делим по символу пробел
                min_salary = None  # минимальная зп
                max_salary = int(''.join(_mid))  # объединяем элементы списка и преобразуем в число
                curency = _salary[-1]  # тип валюты
            else:  # если и нижняя и верхняя зп
                _salary = _salary.split(' ')  # делим строку по символу пробел
                _left = _salary[1].split('\xa0')  # левая часть - минимальная зп: делим строку по символу пробел
                min_salary = int(''.join(_left))  # объединяем элементы списка и преобразуем в число
                _right = _salary[3].split(
                    '\xa0')  # правая часть - минимальная зп и валюта: делим строку по символу пробел
                curency = _salary[-1]  # тип валюты
                # _right = _right.split('\xa0')  # вновь разбиваем по пробелу
                max_salary = int(''.join(_right))  # объединяем элементы списка и преобразуем в число
        else:
            min_salary = None
            max_salary = None
            curency = None
        return min_salary, max_salary, curency

    def Salary_sj(self, item: JobparserItem):
        """"
        Для сайта суперджоб
        Функция возвращает три переменные - минимальная зп, максимальная зп, валюта
        """
        _salary = item['salary']
        if 'от' in _salary:
            _salary = _salary[2].split('\xa0')  # берем число и делим по символу пробел
            min_salary = int(''.join(_salary[:2]))  # объединяем элементы списка и преобразуем в число
            max_salary = None  # максимальная зп
            curency = _salary[-1]  # тип валюты

        elif 'до' in _salary:
            _salary = _salary[2].split('\xa0')  # берем число и делим по символу пробел
            min_salary = None  # максимальная зп
            max_salary = int(''.join(_salary[:2]))  # объединяем элементы списка и преобразуем в число
            curency = _salary[-1]  # тип валюты

        elif 'По договорённости' in _salary:
            min_salary = None
            max_salary = None
            curency = None

        else:
            min_salary = int(_salary[0].replace('\xa0', ''))  # заменяем неразрывный пробел
            max_salary = int(_salary[1].replace('\xa0', ''))  # заменяем неразрывный пробел
            curency = _salary[-1]  # тип валюты

        return min_salary, max_salary, curency

    def process_item(self, item: JobparserItem, spider):
        collection = self.mongo_base[spider.name]
        if spider.name == 'hhru':
            item['website'] = 'hh.ru'
            item['min_salary'], item['max_salary'], item['curency'] = self.Salary_hh(item)
            collection.insert_one(item)
        elif spider.name == 'sjru':
            item['website'] = 'sjru'
            item['min_salary'], item['max_salary'], item['curency'] = self.Salary_sj(item)
            collection.insert_one(item)
        return item

# def salary(self, item: JobparserItem):
#      """"
#      Функция возвращает три переменные - минимальная зп, максимальная зп, валюта
#      """
#      self._salary = item.get('salary')
#      if self._salary != 'з/п не указана':
#          if 'от ' in self._salary and 'до ' not in self._salary:  # если у нас только нижняя зп
#              self._salary = self._salary.split(' ')  # делим строку по символу пробел
#              self._mid = self._salary[1].split('\u202f')  # берем число и делим по символу пробел
#              self.min_salary = int(''.join(self._mid))  # объединяем элементы списка и преобразуем в число
#              self.max_salary = None  # максимальная зп
#              self.curency = self._salary[-1]  # тип валюты
#          elif 'от ' not in self._salary and 'до ' in self._salary:  # если у нас только верхняя зп
#              self._salary = self._salary.split(' ')  # делим строку по символу пробел
#              self._mid = self._salary[1].split('\u202f')  # берем число и делим по символу пробел
#              self.min_salary = None  # минимальная зп
#              self.max_salary = int(''.join(self._mid))  # объединяем элементы списка и преобразуем в число
#              self.curency = self._salary[-1]  # тип валюты
#          else:  # если и нижняя и верхняя зп
#              self._salary = self._salary.split(' ')  # делим строку по символу пробел
#              self._left = self._salary[0].split('\u202f')  # левая часть - минимальная зп: делим строку по символу пробел
#              self.min_salary = int(''.join(self._left))  # объединяем элементы списка и преобразуем в число
#              self._right = self._salary[1].split(' ')  # правая часть - минимальная зп и валюта: делим строку по символу пробел
#              self.curency = self._right[-1]  # тип валюты
#              self._right = self._right[0].split('\u202f')  # вновь разбиваем по пробелу
#              self.max_salary = int(''.join(self._right))  # объединяем элементы списка и преобразуем в число
#      else:
#          self.min_salary = None
#          self.max_salary = None
#          self.curency = None
#      return self.min_salary, self.max_salary, self.curency
