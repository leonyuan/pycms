#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from account.model import User
from blog.model import Template, Category
from common import DBSession


def init():
    session = DBSession()

    t = session.query(Template).first()

    c1 = Category(u'新闻', 'news')
    c1.template = t

    c2 = Category(u'国内新闻', 'natnews')
    c2.parent = c1
    c2.template = t

    session.add(c1)
    session.add(c2)
    session.commit()

if __name__ == '__main__':
    init()
