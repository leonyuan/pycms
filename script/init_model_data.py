#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Model, Field, Relation
from common import DBSession


def init():
    session = DBSession()

    job = Model(name='job', title=u'职位')
    title = Field(name='title', title=u'名称', type='string', length=32)
    point = Field(name='point', title=u'点击数', type='integer', length=-1)
    job.fields.append(title)
    job.fields.append(point)

    #r1 = Relation(name='category', title=u'栏目', type='many-to-one', target='Category', backref='jobs')
    r1 = Relation(name='categories', title=u'栏目', type='many-to-many', target='Category', backref='jobs')
    job.relations.append(r1)

    session.add(job)
    session.commit()

if __name__ == '__main__':
    init()
