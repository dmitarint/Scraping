"""
1.	написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. для
парсинга использовать xpath. структура данных должна содержать:
o	название источника;
o	наименование новости;
o	ссылку на новость;
o	дата публикации.
2.	сложить собранные данные в бд
минимум один сайт, максимум - все три
"""

from pymongo import MongoClient
import requests
from lxml import html

def get_news(news_link):
    """
    Функция принимает на вход ссылку, и возвращает название новости, короткое описание и дату
    """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
    news_response = requests.get(news_link, headers=header)
    news_dom = html.fromstring(news_response.text)
    news_title = news_dom.xpath(
        "//h1[@class='hdr__inner']/text()")  # Название новости
    news_title = "".join(news_title).replace('\xa0', ' ')  # Преобразуем в текст, заменим неразрывные пробелы
    news_brief = news_dom.xpath("//div[@class='article__intro meta-speakable-intro']//text()")  # Короткое описание
    news_brief = "".join(news_brief).replace('\xa0', ' ')  # Преобразуем в текст, заменим неразрывные пробелы
    news_date = news_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]  # Дата публикации
    return news_title, news_brief, news_date


client = MongoClient('localhost', 27017)
db = client['news']  # Задаим имя базы данных
collection = db.mail  # Коллекция только для сайта мейл. Потом можно будет расширить

url = 'https://news.mail.ru/'  # Ссылка на сайт мейла
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0)'
                  ' Gecko/20100101 Firefox/90.0'}  # Клиент файерфокса
response = requests.get(url, headers=header)

dom = html.fromstring(response.text)

mail_news = {}

# Спарсим первую новость
news_link = dom.xpath("//td[@class='daynews__main']//@href")  # ссылка на первую новость в главном блоке
mail_news['title'], \
mail_news['brief'], \
mail_news['date'] = get_news(news_link[0])
mail_news['link'] = news_link[0]
mail_news['source'] = 'mail.ru'
collection.update_one({'link': mail_news['link']},  # Обновим коллекцию
                      {'$set': mail_news}, upsert=True)

# Спарсим второй блок новостей
main_block_news_links = dom.xpath("//td[@class='daynews__items']/div[@class='daynews__item']//@href")
for news in main_block_news_links:
    mail_news['title'], \
    mail_news['brief'], \
    mail_news['date'] = get_news(news)
    mail_news['link'] = news
    mail_news['source'] = 'mail.ru'
    collection.update_one({'link': mail_news['link']},  # Обновим коллекцию
                          {'$set': mail_news}, upsert=True)

# Спарсим третий блок новостей
second_block_news_links = dom.xpath(
    "//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']//@href")
for news in second_block_news_links:
    mail_news['title'], \
    mail_news['brief'], \
    mail_news['date'] = get_news(news)
    mail_news['link'] = news
    mail_news['source'] = 'mail.ru'
    collection.update_one({'link': mail_news['link']},  # Обновим коллекцию
                          {'$set': mail_news}, upsert=True)
