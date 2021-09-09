# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaItem(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    user_fullname = scrapy.Field()
    subuser_type = scrapy.Field()
    subuser_id = scrapy.Field()
    subuser_fullname = scrapy.Field()
    subuser_link_to_pic = scrapy.Field()