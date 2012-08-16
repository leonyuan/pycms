#encoding=utf-8
'''
Category and Entity model defination.
'''

import web
from sqlalchemy import Table, Column, Integer, String, DateTime, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from pycms.db.util import Base
from pycms.template.model import Template


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    slug = Column(String(32), nullable=False)
    parent_id = Column(Integer, ForeignKey('category.id'))
    template_id = Column(Integer, ForeignKey('template.id'))

    template = relationship('Template', backref=backref('categories'))
    children = relationship("Category", order_by=id, cascade='delete', backref=backref('parent', remote_side=[id]))

    def __repr__(self):
        return "<Category(%d '%s')>" % (self.id, self.name)


