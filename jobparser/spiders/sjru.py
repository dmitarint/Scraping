import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['www.superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=pyhon&geo[t][0]=4&page=0']

    def parse(self, response: HtmlResponse):
        if response.xpath("//*[contains(*,'Ничего не нашлось')]"):
            pass
        else:
            links = response.xpath("//a[contains(@class,'icMQ_ _6AfZ9 f-test-link-')]/@href").extract()
            page = int(response.url[-1]) #  берем последний сивол ссылки
            page += 1 #  добавляем страницу
            next_page = response.url[:-1] + str(page) #  формируем новую ссылку
            yield response.follow(next_page, callback=self.parse)
            for link in links:
                yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response):
        vac_name = response.xpath("//h1/text()").extract_first()
        vac_salary = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        vac_url = response.url
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)

        pass

