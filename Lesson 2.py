"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
 с сайтов HH(обязательно) и/или Superjob(по желанию).
 Приложение должно анализировать несколько страниц сайта
 (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
    1.	Наименование вакансии.
    2.	Предлагаемую зарплату (отдельно минимальную и максимальную).
    3.	Ссылку на саму вакансию.
    4.	Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
 Сохраните в json либо csv.
"""

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from pymongo import MongoClient


def salary(vac):
    """"
    Функция возвращает три переменные - минимальная зп, максимальная зп, валюта
    """
    try:
        _salary = vac.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
        if 'от ' in _salary:  # если у нас только нижняя зп
            _salary = _salary.split(' ')  # делим строку по символу пробел
            _mid = _salary[1].split('\u202f')  # берем число и делим по символу пробел
            min_salary = int(''.join(_mid))  # объединяем элементы списка и преобразуем в число
            max_salary = None  # максимальная зп
            curency = _salary[-1]  # тип валюты
        elif 'до ' in _salary:  # если у нас только верхняя зп
            _salary = _salary.split(' ')  # делим строку по символу пробел
            _mid = _salary[1].split('\u202f')  # берем число и делим по символу пробел
            min_salary = None  # минимальная зп
            max_salary = int(''.join(_mid))  # объединяем элементы списка и преобразуем в число
            curency = _salary[-1]  # тип валюты
        else:  # если и нижняя и верхняя зп
            _salary = _salary.split(' ')  # делим строку по символу пробел
            _left = _salary[0].split('\u202f')  # левая часть - минимальная зп: делим строку по символу пробел
            min_salary = int(''.join(_left))  # объединяем элементы списка и преобразуем в число
            _right = _salary[1].split(' ')  # правая часть - минимальная зп и валюта: делим строку по символу пробел
            curency = _right[-1]  # тип валюты
            _right = _right[0].split('\u202f')  # вновь разбиваем по пробелу
            max_salary = int(''.join(_right))  # объединяем элементы списка и преобразуем в число
    except:
        min_salary = None
        max_salary = None
        curency = None
    return min_salary, max_salary, curency


client = MongoClient('localhost', 27017)  # Подключим клиент Монго
db = client['hh_db']
collection = db.hh

# Зададим адрес сайта и заголовок юзер-агента
url = 'https://hh.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
# https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=%D0%BF%D0%B8%D1%82%D0%BE%D0%BD

input_salary = None  # Пока зарплату оставим None. Задается целочисленное минимальное значение
# vacancy = input('Введите должность: ')
vacancy = 'водитель'  # создадим переменную с названием вакансии
not_final_page = True  # условие проверки на последнюю страницу сайта
page = 0    # зададим стартовую станицу

while not_final_page:  # Цикл для того, чтобы пройтись по всем страницам с вакансиями
    # Зададим параметры
    params = {'clusters': 'true',
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'salary': input_salary,
              'st': 'searchVacancy',
              'text': vacancy,
              'area': None,  # Все вакансии. Для Москвы ввести 1
              'page': page
              }
    page += 1  # Прибавляем иттерацию страницы
    response = requests.get(url + 'search/vacancy', params=params, headers=headers)  # отправим запрос гет с заголовками и параметрами
    soup = bs(response.text, 'html.parser')  # преобразуем ответ сервера в суп
    # Проверим, является ли страница последней
    if len(soup.find_all('a', attrs={'class': 'bloko-button', 'data-qa': 'pager-next'})) == 0:  #  есть ли кнопка далее?
        not_final_page = False

    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})  # находим блоки с вакансиями

    for vac in vacancy_list:  # вытащим название вакансии, ссылку, зарплаты, имя компании
        info_vacancies = {}
        info_vacancies['name'] = vac.find('span', attrs={'class': 'g-user-content'}).getText()
        info_vacancies['url_vac'] = vac.find('a', attrs={'class': 'bloko-link'}).get('href')
        info_vacancies['min_salary'], info_vacancies['max_salary'], info_vacancies['curency'] = salary(vac)
        info_vacancies['company_name'] = vac.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).getText()
        if collection.find_one(info_vacancies) is not None:   # проверим есть ли вакансия в базе Монго
            continue
        collection.insert_one(info_vacancies)

#  Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
def find_vacancy(desirable_salary, desirable_curency = 'руб.'):
    desirable_salary = int(desirable_salary)
    #  Осуществляем поиск вакансий, у которых совпадает валюта и минимальная или максимальная зп больше, чем задано
    vacancies = collection.find({'curency': desirable_curency,
                         '$or':
                             [
                             {'min_salary': {'$gte': desirable_salary}
                             },
                             {'max_salary':{'$gte': desirable_salary}
                             }
                             ]
                         })
    return list(vacancies)


for i in find_vacancy(100000):
    print (' ')
    pprint(i)