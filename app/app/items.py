# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime


def remove_quotes(text):
    text = text.strip(u'\u201c'u'\u201d')
    return text


def create_full_link(relative_link):
    full_link = 'http://quotes.toscrape.com' + relative_link
    return full_link


def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y').date()


def find_initials(text: str):
    initials = []
    for letter in text:
        if letter == letter.upper() and letter.isalpha():
            initials.append(letter)

    return '. '.join(initials)


class QuoteItem(Item):
    author = Field(
        output_processor=TakeFirst()
    )
    quote = Field(input_processor=MapCompose(
        remove_quotes), output_processor=TakeFirst())
    tags = Field()
    author_link = Field(input_processor=MapCompose(
        create_full_link), output_processor=TakeFirst())


class AuthorItem(Item):

    name = Field(
        output_processor=TakeFirst()
    )
    initials = Field(
        input_processor=MapCompose(find_initials),
        output_processor=TakeFirst()
    )
    birthday = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    info = Field(
        output_processor=TakeFirst()
    )
