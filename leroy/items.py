# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def params_transformation(value):
    n = len(value)//2  # в Айтемлоадер попадают ключи и атрибуты одним списком. Делим его на 2
    _value = []
    _value.append(value[:n])
    _value.append(value[n:])
    for i in range(len(_value[1])): # убирем из второй части пробелы
        _value[1][i] = _value[1][i].replace("\n                ", "").replace('\n            ', '')
    value = dict(zip(_value[0], _value[1]))  # создаем словарь
    return value

class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(output_processor=params_transformation)
    # params_attr = scrapy.Field()
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    curency = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
    # pass
