import scrapy
from scrapy.loader import ItemLoader
from app.items import QuoteItem


class QuotesSpider(scrapy.Spider):

    name = 'quotes'

    custom_settings = {
        'ITEM_PIPELINES': {
            'app.pipelines.DuplicateQuotePipeline': 100,
            'app.pipelines.SaveQuotesPipeline': 200
        }
    }

    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):

        for quote in response.xpath("//div[@class='quote']"):
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_xpath('author', "span/small/text()")
            loader.add_xpath('quote', "span[@class='text']/text()")
            loader.add_xpath('tags', "div[@class='tags']/a/text()")
            loader.add_xpath(
                'author_link', "span/a/@href")
            yield loader.load_item()

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(url=response.urljoin(next_link), callback=self.parse)
