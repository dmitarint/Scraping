from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.spiders.avito import AvitoSpider
from avitoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    # input = ('')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoSpider, search='велосипед')

    process.start()