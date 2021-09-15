import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader


class LeroySSpider(scrapy.Spider):
    name = 'leroy_s'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/']

    def __init__(self, search):
        super(LeroySSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&suggest=true']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label,'Следующая страница:')]/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@alt = 'product image']/@src")
        print()
        loader.add_xpath('params', "//dt[@class = 'def-list__term']/text()")
        loader.add_xpath('params',  "//dd[@class = 'def-list__definition']/text()")
        # loader.add_xpath('params_attr', )
        loader.add_xpath('price', "//uc-pdp-price-view//meta[@itemprop='price']/@content")
        loader.add_xpath('curency', "//uc-pdp-price-view//meta[@itemprop='priceCurrency']/@content")
        loader.add_value('url', response.url)
        yield loader.load_item()
