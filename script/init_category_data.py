#encoding=utf-8
from basis.model import Category
from models.model import Model
from common import DBSession


def init():
    session = DBSession()

    #m1 = session.query(Model).get(1)
    #m2 = session.query(Model).get(2)

    c1 = Category(name=u'新闻', slug='news')
    #c1.model = m2

    c2 = Category(name=u'国内新闻', slug='natnews')
    c2.parent = c1
    #c2.model = m2

    c3 = Category(name=u'猎头职位', slug='medicine_jobs')
    #c3.model = m1

    session.add(c1)
    session.add(c2)
    session.add(c3)
    session.commit()

if __name__ == '__main__':
    init()
