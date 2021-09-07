# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    website = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    curency = scrapy.Field()


