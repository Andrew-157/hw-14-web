# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_quotes(text):
    text = text.strip(u'\u201c'u'\u201d')
    return text


def create_full_link(relative_link):
    full_link = 'http://quotes.toscrape.com' + relative_link
    return full_link


class QuoteItem(Item):
    author = Field(
        output_processor=TakeFirst()
    )
    quote = Field(input_processor=MapCompose(
        remove_quotes), output_processor=TakeFirst())
    tags = Field()
    author_link = Field(input_processor=MapCompose(
        create_full_link), output_processor=TakeFirst())
