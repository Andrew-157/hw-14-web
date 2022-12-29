# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from app.models import connect_db, create_engine, create_table, Quote, Author, Tag
from sqlalchemy.orm import sessionmaker


class QuotePipeline:

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
