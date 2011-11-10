'''
Account model defination.
'''

import web
from sqlalchemy import Table, Column, SmallInteger, Integer, Boolean, String, DateTime, TIMESTAMP, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

from account.util import check_password, get_hexdigest
from common import Base, engine
from common.dbutil import utcnow


class Session(Base):
    __tablename__ = 'session'
    session_id = Column(String(128), primary_key=True)
    atime  = Column(TIMESTAMP, default=utcnow())
    data = Column(Text)

    def __init__(self, sid):
        self.session_id = sid

    def __repr__(self):
        return "<Session('%s')>" % (self.session_id)


permission_group_asso_table = Table('permission_group_asso', Base.metadata,
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True)
)

permission_user_asso_table = Table('permission_user_asso', Base.metadata,
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    codename = Column(String(64), nullable=False)
    order = Column(SmallInteger)
    parent_id = Column(Integer, ForeignKey('permission.id'))

    children = relationship("Permission", backref=backref('parent', remote_side=[id]))
    groups = relationship("Group", secondary=permission_group_asso_table, backref=backref('permissions'))
    users = relationship("User", secondary=permission_user_asso_table, backref=backref('permissions'))

    def __init__(self, name, codename):
        self.name = name
        self.codename = codename

    def url(self):
        l = self.codename.split('_')
        return '/'.join(l)

    #def __repr__(self):
    #    return "<Permission('%s', '%s')>" % (self.name, self.codename)

    def __unicode__(self):
        return "<Permission('%s', '%s')>" % (self.name, self.codename)

group_user_asso_table = Table('group_user_asso', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    users = relationship("User", secondary=group_user_asso_table, backref=backref('groups'))

    #def __init__(self, name):
    #    self.name = name

    def __repr__(self):
        return "<Group('%s')>" % (self.name)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_login = Column(TIMESTAMP, default=utcnow())
    joined_time = Column(TIMESTAMP, default=utcnow())

    '''def __init__(self, username, email):
        self.username = username
        self.email = email'''

    def set_password(self, raw_password):
        import random
        salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(salt, raw_password)
        self.password = '%s$%s' % (salt, hsh)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password);

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.username, self.email)


permission_table = Permission.__table__
group_table = Group.__table__
user_table = User.__table__
metadata = Base.metadata


if __name__ == "__main__":
    metadata.create_all(engine)
