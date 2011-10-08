#encoding=utf-8
import web
from sqlalchemy import func
from models.model import *
from common.dbutil import populate
from models.util import build_model
from basis.dbutil import get_category, get_category_ancestors

#-------------------------------
# some utility
#-------------------------------

#-------------------------------
# model persistent method
#-------------------------------
def get_models():
    return web.ctx.orm.query(Model).all()

def get_model_by_name(name):
    return web.ctx.orm.query(Model).filter_by(name=name).first()

def get_model(id):
    return web.ctx.orm.query(Model).get(id)

def save_model(id, data):
    if id == -1:
        model = Model()
    else:
        model = get_model(id)

    populate(model, data, Model)

    if id == -1:
        web.ctx.orm.add(model)
    else:
        web.ctx.orm.flush()

def del_model(id):
    model = get_model(id)
    web.ctx.orm.delete(model)

def activate_model(model):
    model.is_active = True
    web.ctx.orm.flush()

def inactivate_model(model):
    model.is_active = False
    web.ctx.orm.flush()


#-------------------------------
# field persistent method
#-------------------------------
def get_fields(mid):
    return web.ctx.orm.query(Field).filter_by(model_id=mid).order_by(Field.id).all()

def get_field(id):
    return web.ctx.orm.query(Field).get(id)

def save_field(id, data):
    if id == -1:
        field = Field()
    else:
        field = get_field(id)

    populate(field, data, Field)

    if id == -1:
        web.ctx.orm.add(field)
    else:
        web.ctx.orm.flush()

def del_field(id):
    field = get_field(id)
    web.ctx.orm.delete(field)

#-------------------------------
# relation persistent method
#-------------------------------
def get_relations(mid):
    return web.ctx.orm.query(Relation).filter_by(model_id=mid).order_by(Relation.id).all()

def get_relation(id):
    return web.ctx.orm.query(Relation).get(id)

def save_relation(id, data):
    if id == -1:
        relation = Relation()
    else:
        relation = get_relation(id)

    populate(relation, data, Relation)

    if id == -1:
        web.ctx.orm.add(relation)
    else:
        web.ctx.orm.flush()

def del_relation(id):
    relation = get_relation(id)
    web.ctx.orm.delete(relation)

#-------------------------------
# entity persistent method
#-------------------------------
def get_entities(model, cid=None, limit=None):
    model_cls = build_model(model)
    if cid is None:
        return web.ctx.orm.query(model_cls).order_by(model_cls.id.desc()).all()
    else:
        if limit is None:
            return web.ctx.orm.query(model_cls).filter(model_cls.categories.any(id=cid)).order_by(model_cls.id.desc()).all()
        else:
            return web.ctx.orm.query(model_cls).filter(model_cls.categories.any(id=cid)).order_by(model_cls.id.desc()).limit(limit)

def get_entity(model, id):
    model_cls = build_model(model)
    return web.ctx.orm.query(model_cls).get(id)

def new_entity(model, data):
    save_entity(model, -1, data)

def save_entity(model, id, data):
    model_cls = build_model(model)
    if id == -1:
        entity = model_cls()
    else:
        entity = get_entity(model, id)

    populate(entity, data, model_cls)

    cid = data.cid
    category = get_category(cid)
    entity.categories.append(category)

    if id == -1:
        web.ctx.orm.add(entity)
    else:
        web.ctx.orm.flush()

def del_entity(model, id):
    entity = get_entity(model, id)
    web.ctx.orm.delete(entity)

def get_entitys_category_ancestors(entity):
    return get_category_ancestors(entity.categories[0])

def get_latest_entities(mname, cid, count):
    model = get_model_by_name(mname)
    return get_entities(model, cid, count)


