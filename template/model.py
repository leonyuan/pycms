#encoding=utf-8
'''
Template model defination.
'''

import web
from sqlalchemy import Table, Column, Integer, String

from pycms.db.util import Base, utcnow


class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    index_file = Column(String(100), nullable=False)
    list_file = Column(String(100), nullable=False)
    display_file = Column(String(100), nullable=False)

    def __repr__(self):
        return "<Template('%s')>" % (self.name)

