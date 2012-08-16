#encoding=utf-8
'''
Customized model defination.
'''

import web
from sqlalchemy import Table, Column, Integer, Boolean, String, DateTime, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred

from pycms.db.util import Base, utcnow
from pycms.template.model import Template


category_entity_asso_table = Table('category_entity_asso', Base.metadata,
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('entity_id', Integer, ForeignKey('entity.id'), primary_key=True)
)

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    slug = Column(String(32))
    status = Column(String(8))
    created_time = Column(TIMESTAMP, default=utcnow())
    user_id = Column(Integer, ForeignKey('user.id'))
    model_id = Column(Integer, ForeignKey('model.id'))

    user = relationship('User', backref=backref('entities'))
    model = relationship('Model', backref=backref('entities'))
    categories = relationship("Category", secondary=category_entity_asso_table, backref=backref('entities'))

    def __repr__(self):
        return "<Entity('%s')>" % (self.title)

class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    title = Column(String(32))
    description = Column(String(255))
    is_active = Column(Boolean, default=False)
    template_id = Column(Integer, ForeignKey('template.id'))
    parent_id = Column(Integer, ForeignKey('model.id'))

    template = relationship('Template', backref=backref('models'))
    children = relationship("Model", order_by=id, cascade='delete', backref=backref('parent', remote_side=[id]))
    fields = relationship("Field", cascade='delete', backref=backref('model'))
    relations = relationship("Relation", cascade='delete', backref=backref('model'))

    def __repr__(self):
        return "<Model('%s')>" % (self.name)

class Field(Base):
    __tablename__ = 'model_field'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    title = Column(String(32))
    type = Column(String(16), nullable=False)
    length = Column(Integer)
    required = Column(Boolean)
    props = Column(Text)
    model_id = Column(Integer, ForeignKey('model.id'))

    def __repr__(self):
        return "<Field('%s')>" % (self.name)

class Relation(Base):
    __tablename__ = 'model_relation'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    title = Column(String(32))
    type = Column(String(16), nullable=False)
    target = Column(String(16))
    backref = Column(String(16))
    secondary = Column(String(16))

    model_id = Column(Integer, ForeignKey('model.id'))

    def __repr__(self):
        return "<Relation('%s')>" % (self.name)

