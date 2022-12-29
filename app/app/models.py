from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, Date
from scrapy.utils.project import get_project_settings


Base = declarative_base()


def connect_db():

    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


quote_tag = Table('quote_tag', Base.metadata,
                  Column('quote_id', Integer, ForeignKey('quote.id')),
                  Column('tag_id', Integer, ForeignKey('tag.id'))
                  )


class Quote(Base):

    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    quote_text = Column('quote_text', Text())
    author_id = Column(Integer, ForeignKey('author.id'))
    tags = relationship('Tag', secondary='quote_tag',
                        lazy='dynamic', backref='quote')


class Author(Base):

    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    link = Column(String(50), unique=True)
    quotes = relationship('Quote', backref='author')


class Tag(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    quotes = relationship('Quote', secondary='quote_tag',
                          lazy='dynamic', backref='tag')


class AuthorInfo(Base):

    __tablename__ = 'author_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    initials = Column(String(10))
    birthday = Column(Date)
    info = Column('info', Text())



