#encoding=utf-8
from basis.model import Template
from models.model import Model, Field, Relation
from common import DBSession


def init():
    session = DBSession()

    t1 = session.query(Template).filter_by(name=u'新闻模板').first()
    t2 = session.query(Template).filter_by(name=u'职位模板').first()

    job = Model(name='job', title=u'职位')
    job.template = t2

    #title = Field(name='title', title=u'名称', type='string', length=32, required=True)
    point = Field(name='point', title=u'点击数', type='integer')
    content1 = Field(name='content', title=u'内容', type='text')

    #session.add(title)
    session.add(point)
    session.add(content1)

    #job.fields.append(title)
    job.fields.append(point)
    job.fields.append(content1)

    #r1 = Relation(name='user', title=u'创建者', type='many-to-one', target='User', backref='jobs')
    #r2 = Relation(name='categories', title=u'栏目', type='many-to-many', target='Category', backref='jobs')

    #session.add(r1)
    #session.add(r2)

    #job.relations.append(r1)
    #job.relations.append(r2)

    session.add(job)


    news = Model(name='news', title=u'新闻')
    news.template = t1

    #title = Field(name='title', title=u'标题', type='string', length=32, required=True)
    keywords = Field(name='keywords', title=u'关键词', type='string', length=64)
    summary = Field(name='summary', title=u'摘要', type='string', length=255)
    content2 = Field(name='content', title=u'内容', type='text')

    #session.add(title)
    session.add(keywords)
    session.add(summary)
    session.add(content2)

    #news.fields.append(title)
    news.fields.append(keywords)
    news.fields.append(summary)
    news.fields.append(content2)

    #r3 = Relation(name='user', title=u'创建者', type='many-to-one', target='User', backref='news')
    #r4 = Relation(name='categories', title=u'栏目', type='many-to-many', target='Category', backref='news')

    #session.add(r3)
    #session.add(r4)

    #news.relations.append(r3)
    #news.relations.append(r4)

    session.add(news)

    session.commit()

if __name__ == '__main__':
    init()
