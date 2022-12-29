# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_quotes(text):
    text = text.strip(u'\u201c'u'\u201d')
    return text


class QuoteItem(Item):
    author = Field()
    quote = Field(
        input_processor=MapCompose(remove_quotes)
    )
    tags = Field()
    author_link = Field()
