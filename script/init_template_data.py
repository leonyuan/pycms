#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from blog.model import Template
from common import DBSession


def init():
    session = DBSession()

    t1 = Template(name=u'新闻模板')
    t1.file = 'templates/template/news.html'

    t2 = Template(name=u'博客模板')
    t2.file = 'templates/template/blog.html'

    session.add(t1)
    session.add(t2)
    session.commit()

if __name__ == '__main__':
    init()
