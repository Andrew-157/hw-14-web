import scrapy


class QuotesSpider(scrapy.Spider):

    name = 'quotes'

    allowed_domains = ['quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):

        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'author': quote.xpath("span/small/text()").get(),
                'quote': quote.xpath("span[@class='text']/text()").get(),
                'tags': quote.xpath("div[@class='tags']/a/text()").extract(),
                'author_link': self.start_urls[0] + quote.xpath("span/a/@href").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
