#encoding=utf-8
'''
Blog model defination.
'''

import web
from sqlalchemy import Table, Column, Integer, String, DateTime, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred

from common import Base, engine
from common.dbutil import utcnow
from account.model import User
from models.model import Model

class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    index_file = Column(String(100), nullable=False)
    list_file = Column(String(100), nullable=False)
    display_file = Column(String(100), nullable=False)

    def __repr__(self):
        return "<Template('%s')>" % (self.name)

category_entity_asso_table = Table('category_entity_asso', Base.metadata,
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('entity_id', Integer, ForeignKey('entity.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    slug = Column(String(32), nullable=False)
    parent_id = Column(Integer, ForeignKey('category.id'))

    children = relationship("Category", order_by=id, cascade='delete', backref=backref('parent', remote_side=[id]))
    entities = relationship("Entity", secondary=category_entity_asso_table, backref=backref('categories'))

    def __repr__(self):
        return "<Category('%s')>" % (self.name)

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    slug = Column(String(32))
    status = Column(String(8))
    created_time = Column(TIMESTAMP, default=utcnow())
    user_id = Column(Integer, ForeignKey('user.id'))
    model_id = Column(Integer, ForeignKey('model.id'))

    user = relationship(User, backref=backref('entities'))
    model = relationship(Model, backref=backref('entities'))

    def __repr__(self):
        return "<Entity('%s')>" % (self.title)


template_table = Template.__table__
category_table = Category.__table__
metadata = Base.metadata


if __name__ == "__main__":
    metadata.create_all(engine)
