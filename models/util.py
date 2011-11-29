import web
from copy import deepcopy
from sqlalchemy import ForeignKey, Table, Column, SmallInteger, Integer, Float, Boolean,\
        String, DateTime, TIMESTAMP, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from common import Base, engine
from account.model import User
from basis.model import Category, Entity
from sqlalchemy.orm import scoped_session
from common import DBSession
from models.model import Model


DEFAULT_ATTR = {
        'id': Column(Integer, primary_key=True),
}

FIELD_TYPE = {
    'string': String,
    'integer': Integer,
    'text': Text,
    'float': Float,
    'boolean': Boolean,
    'select': String,
    'radio': String,
    'checkbox': String,
    'date': DateTime,
    'datetime': TIMESTAMP,
}

class _cache_relation(object):
    def __init__(self, name, type, target, backref):
        self.name = name
        self.type = type
        self.target = target
        self.backref = backref

class _cache_model(object):
    def __init__(self, model):
        self.id = model.id
        self.name = model.name
        self.relations = []
        if model.relations is not None:
            for rel in model.relations:
                self.relations.append(_cache_relation(rel.name, rel.type, rel.target, rel.backref))


_models_cache = {}

def build_model(model, refresh=False):
    sid = str(model.id)
    if sid in _models_cache and not refresh:
        return _models_cache[sid]['cls']
    else:
        remove_model_from_cache(sid)
        attrs = {}
        attrs.update(deepcopy(DEFAULT_ATTR))
        attrs['__tablename__'] = model.name
        asso_tables = []
        for field in model.fields:
            fld_type = FIELD_TYPE[field.type]
            if field.length and field.length != -1:
                fld_type = fld_type(field.length)
            fld_attr = {field.name: Column(fld_type)}
            attrs.update(fld_attr)

        #the default entity relation
        attrs['entity_id'] = Column(Integer, ForeignKey('entity.id'))
        attrs['entity'] = relationship('Entity', backref=backref(model.name.lower(), uselist=False))

        for rel in model.relations:
            if rel.type == 'many-to-one':
                parent_model_name = rel.target.lower()
                foreign_key = {'%s_id' % parent_model_name : Column(Integer, ForeignKey('%s.id' % parent_model_name))}
                rel_attr = {rel.name: relationship(rel.target, backref=backref(rel.backref))}
                attrs.update(foreign_key)
                attrs.update(rel_attr)
            elif rel.type == 'many-to-many':
                parent_model_name = rel.target.lower()
                asso_table =Table('%s_%s_asso' % (parent_model_name, model.name), Base.metadata,\
                    Column('%s_id' % parent_model_name, Integer, ForeignKey('%s.id' % parent_model_name), primary_key=True),
                    Column('%s_id' % model.name, Integer, ForeignKey('%s.id' % model.name), primary_key=True)
                )
                asso_tables.append(asso_table)
                if rel.backref is not None:
                    rel_attr = {rel.name: relationship(rel.target, secondary=asso_table, backref=backref(rel.backref))}
                else:
                    rel_attr = {rel.name: relationship(rel.target, secondary=asso_table)}

                attrs.update(rel_attr)

        cls = type(str(model.name), (Base,), attrs)
        cls.asso_tables = asso_tables
        cache_model = _cache_model(model)
        _models_cache[sid] = dict(cls=cls, model=cache_model)
        return cls

def remove_model_from_cache(sid):
    if sid in _models_cache:
        cls = _models_cache[sid]['cls']
        cache_model = _models_cache[sid]['model']
        del cls.__mapper__.get_property('entity').mapper._props[cache_model.name.lower()]
        for rel in cache_model.relations:
            if rel.backref is not None:
                if cls.__mapper__.has_property(rel.name) and rel.backref in cls.__mapper__.get_property(rel.name).mapper._props:
                    del cls.__mapper__.get_property(rel.name).mapper._props[rel.backref]
        cls.__mapper__.dispose()

        for asso_table in cls.asso_tables:
            Base.metadata.remove(asso_table)
        Base.metadata.remove(cls.__table__)

        _models_cache[sid].clear()
        del _models_cache[sid]

def create_schema(model):
    cls = build_model(model, True)
    cls.__table__.create(engine, checkfirst=True)
    for asso_table in cls.asso_tables:
        asso_table.create(engine, checkfirst=True)

def drop_schema(model):
    cls = build_model(model)
    remove_model_from_cache(str(model.id))
    for asso_table in cls.asso_tables:
        asso_table.drop(engine, checkfirst=True)
    cls.__table__.drop(engine, checkfirst=True)

def init_model_class():
    sess = scoped_session(DBSession)
    models = sess.query(Model).filter_by(is_active=True).all()
    for model in models:
        build_model(model)

