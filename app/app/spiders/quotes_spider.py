import scrapy
from scrapy.loader import ItemLoader
from app.items import QuoteItem


class QuotesSpider(scrapy.Spider):

    name = 'quotes'

    allowed_domains = ['quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):

        for quote in response.xpath("//div[@class='quote']"):
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_xpath('author', "span/small/text()")
            loader.add_xpath('quote', "span[@class='text']/text()")
            loader.add_xpath('tags', "div[@class='tags']/a/text()")
            loader.add_xpath(
                'author_link', "span/a/@href")

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
