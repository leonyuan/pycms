from sqlalchemy import ForeignKey, Table, Column, SmallInteger, Integer, Boolean, String, DateTime, TIMESTAMP, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from common import Base, engine
from account.model import User
from blog.model import Category

#Base = declarative_base()

DEFAULT_ATTR = {'id':Column(Integer, primary_key=True)}

FIELD_TYPE = {
    'string': String,
    'integer': Integer,
}

def build_model(model):
    attrs = {}
    attrs.update(DEFAULT_ATTR)
    attrs['__tablename__'] = model.name
    for field in model.fields:
        fld_type = FIELD_TYPE[field.type]
        if field.length != -1:
            fld_type = fld_type(field.length)
        fld_attr = {field.name: Column(fld_type)}
        attrs.update(fld_attr)

    for relation in model.relations:
        if relation.type == 'many-to-one':
            parent_model_name = relation.target.lower()
            foreign_key = {'%s_id' % parent_model_name : Column(Integer, ForeignKey('%s.id' % parent_model_name))}
            relation_attr = {relation.name: relationship(relation.target, backref=backref(relation.backref))}
            attrs.update(foreign_key)
            attrs.update(relation_attr)
        elif relation.type == 'many-to-many':
            parent_model_name = relation.target.lower()
            asso_table =Table('%s_%s_asso' % (parent_model_name, model.name), Base.metadata,\
                Column('%s_id' % parent_model_name, Integer, ForeignKey('%s.id' % parent_model_name), primary_key=True),
                Column('%s_id' % model.name, Integer, ForeignKey('%s.id' % model.name), primary_key=True)
            )
            relation_attr = {relation.name: relationship(relation.target, secondary=asso_table, backref=backref(relation.backref))}
            attrs.update(relation_attr)

    cls = type(str(model.name), (Base,), attrs)
    return cls

def create_table(cls):
    Base.metadata.create_all(engine)

def drop_table(cls):
    cls.__table__.drop(engine)
