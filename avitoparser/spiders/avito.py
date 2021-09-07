import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    def __init__(self, search):
        super(AvitoSpider, self).__init__()
        self.start_urls = [f'https://www.avito.ru/izhevsk?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-marker='item-title']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath("name", "//h1/span/text()")
        loader.add_xpath("photos", "//div[@class='gallery-img-frame js-gallery-img-frame']/@data-url")
        loader.add_value("url", response.url)

        yield loader.load_item()
        # name = response.xpath("//h1/span/text()").extract_first()
        # photos = response.xpath("//div[@class='gallery-img-frame js-gallery-img-frame']/@data-url").extract()
        # yield AvitoparserItem(name=name, photos=photos)


