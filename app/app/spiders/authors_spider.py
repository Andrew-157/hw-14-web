import scrapy


class AuthorsSpider(scrapy.Spider):

    name = 'authors'

    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            author_url = quote.xpath("//span/a/@href").get()
            yield response.follow(response.urljoin(author_url), self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(url=response.urljoin(next_link), callback=self.parse)

    def parse_author(self, response):
        for info in response.xpath("//div[@class='author-details']"):
            yield {
                'text': info.xpath("//div[@class='author-description']/text()").get()
            }
