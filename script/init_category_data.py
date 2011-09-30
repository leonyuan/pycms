#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from account.model import User
from blog.model import Category
from models.model import Model
from common import DBSession


def init():
    session = DBSession()

    m = session.query(Model).first()

    c1 = Category(name=u'新闻', slug='news')

    c2 = Category(name=u'国内新闻', slug='natnews')
    c2.parent = c1

    c3 = Category(name=u'猎头职位', slug='medicine_jobs')
    c3.model = m

    session.add(c1)
    session.add(c2)
    session.add(c3)
    session.commit()

if __name__ == '__main__':
    init()
