#encoding=utf-8
'''
Blog model defination.
'''

import web
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from account.util import check_password, get_hexdigest
from common import Base, engine
from common.dbutil import utcnow
from account.model import User


class CategoryArticleAssoc(Base):
    __tablename__ = 'category_article_assoc'
    category_id = Column(Integer, ForeignKey('category.id'), primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'), primary_key=True)
    category = relationship("Category", backref=backref('article_assocs'))


class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    file = Column(String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Template('%s')>" % (self.name)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    slug = Column(String(32), nullable=False)
    template_id = Column(Integer, ForeignKey('template.id'))
    parent_id = Column(Integer, ForeignKey('category.id'))

    template = relationship("Template", backref=backref('categories'))
    children = relationship("Category", order_by=id, cascade='delete', backref=backref('parent', remote_side=[id]))

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def __repr__(self):
        return "<Category('%s')>" % (self.name)


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    summary = Column(Text)
    content = Column(MEDIUMTEXT)
    keywords = Column(String(64))
    thumb = Column(String(100))
    posted_time = Column(TIMESTAMP, default=utcnow())
    updated_time = Column(TIMESTAMP, default=utcnow())
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship(User, backref=backref('entries', order_by=id))
    categories = relationship("CategoryArticleAssoc", backref=backref('article', order_by=id))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "<Article('%s')>" % (self.title)

template_table = Template.__table__
category_table = Category.__table__
article_table = Article.__table__
metadata = Base.metadata


if __name__ == "__main__":
    metadata.create_all(engine)
