import web
from copy import deepcopy
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

_models_cache = {}

def build_model(model, refresh=False):
    sid = str(model.id)
    if sid in _models_cache and not refresh:
        return _models_cache[sid]
    else:
        remove_model_from_cache(sid)
        attrs = {}
        attrs.update(deepcopy(DEFAULT_ATTR))
        attrs['__tablename__'] = model.name
        asso_tables = []
        for field in model.fields:
            web.debug('=====field.name:%s' % field.name)
            fld_type = FIELD_TYPE[field.type]
            if field.length and field.length != -1:
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
                asso_tables.append(asso_table)
                if relation.backref is not None:
                    relation_attr = {relation.name: relationship(relation.target, secondary=asso_table, backref=backref(relation.backref))}
                else:
                    relation_attr = {relation.name: relationship(relation.target, secondary=asso_table)}

                attrs.update(relation_attr)

        cls = type(str(model.name), (Base,), attrs)
        cls.asso_tables = asso_tables
        _models_cache[sid] = cls
        return cls

def remove_model_from_cache(sid):
    if sid in _models_cache:
        cls = _models_cache[sid]
        for asso_table in cls.asso_tables:
            Base.metadata.remove(asso_table)
        Base.metadata.remove(cls.__table__)
        del _models_cache[sid]

def create_schema(cls):
    cls.__table__.create(engine, checkfirst=True)
    for asso_table in cls.asso_tables:
        asso_table.create(engine, checkfirst=True)

def drop_schema(cls):
    for asso_table in cls.asso_tables:
        asso_table.drop(engine, checkfirst=True)
        Base.metadata.remove(asso_table)
    cls.__table__.drop(engine, checkfirst=True)
    Base.metadata.remove(cls.__table__)

