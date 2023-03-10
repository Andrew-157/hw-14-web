# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from app.models import connect_db, create_table, Quote, Author, Tag, AuthorInfo
from sqlalchemy.orm import sessionmaker


class SaveQuotesPipeline:

    def __init__(self):
        engine = connect_db()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        quote = Quote()
        author = Author()
        tag = Tag()
        author.name = item['author']
        quote.quote_text = item['quote']
        author.link = item['author_link']

        author_in_db = session.query(
            Author).filter_by(name=author.name).first()

        if author_in_db:
            quote.author = author_in_db
        else:
            quote.author = author

        if 'tags' in item:
            for tag_name in item['tags']:
                tag = Tag(name=tag_name)
                tag_in_db = session.query(Tag).filter_by(name=tag.name).first()
                if tag_in_db:
                    tag = tag_in_db

                quote.tags.append(tag)

        try:
            session.add(quote)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class DuplicateQuotePipeline:

    def __init__(self):
        engine = connect_db()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        quote_in_db = session.query(Quote).filter_by(
            quote_text=item['quote']).first()
        session.close()
        if quote_in_db:
            raise DropItem(f"Duplicate item found--{item['quote']}")

        else:
            return item


class SaveAuthorInfoPipeline:

    def __init__(self):
        engine = connect_db()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        author = AuthorInfo()
        author.name = item['name']
        author.initials = item['initials']
        author.birthday = item['birthday']
        author.info = item['info']

        author_in_db = session.query(AuthorInfo).filter_by(
            name=item['name']).first()
        if author_in_db:
            return item

        try:
            session.add(author)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
