import scrapy
from scrapy.loader import ItemLoader
from app.items import AuthorItem


class AuthorsSpider(scrapy.Spider):

    name = 'authors'

    custom_settings = {
        'ITEM_PIPELINES': {
            'app.pipelines.SaveAuthorInfoPipeline': 300,
        }
    }

    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for author in response.xpath("//div[@class='quote']"):
            author_url = author.xpath("//span/a/@href").get()
            yield response.follow(response.urljoin(author_url), self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()

        if next_link:
            yield response.follow(url=response.urljoin(next_link), callback=self.parse)

    def parse_author(self, response):
        author_page = response.xpath("//div[@class='author-details']")
        loader = ItemLoader(item=AuthorItem(), selector=author_page)
        loader.add_xpath('name', "h3[@class='author-title']/text()")
        loader.add_xpath('initials', "h3[@class='author-title']/text()")
        loader.add_xpath(
            'birthday', "p/span[@class='author-born-date']/text()")
        loader.add_xpath('info', "div[@class='author-description']/text()")
        yield loader.load_item()
