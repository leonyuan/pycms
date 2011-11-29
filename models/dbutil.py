#encoding=utf-8
import web
from sqlalchemy import func
from models.model import *
from models.util import build_model
from common.dbutil import populate
from basis.model import Entity
from basis.dbutil import get_category, get_category_ancestors, get_entity as get_base_entity

#-------------------------------
# some utility
#-------------------------------

#-------------------------------
# model persistent method
#-------------------------------
def get_models():
    return web.ctx.orm.query(Model).all()

def get_active_models():
    return web.ctx.orm.query(Model).filter_by(is_active=True).all()

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
    if hasattr(data, 'type'):
        if data.type == 'text':
            prop_dict = dict(lines=data.lines, editor=data.editor)
            field.props = str(prop_dict)
        elif data.type == 'select' or data.type == 'radio' or data.type == 'checkbox':
            prop_dict = dict(options=data.options)
            if data.type == 'select':
                prop_dict['is_multisel'] = data.is_multisel
            field.props = str(prop_dict)

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

def new_entity(model, base_data, data):
    save_entity(model, -1, base_data, data)

def save_entity(model, id, base_data, data):
    model_cls = build_model(model)
    if id == -1:
        base_entity = Entity()
        entity = model_cls()
    else:
        base_entity = get_base_entity(id)
        entity = getattr(base_entity, model.name)

    populate(base_entity, base_data, Entity)
    populate(entity, data, model_cls)

    for i in range(len(base_entity.categories)-1,-1,-1):
        del base_entity.categories[i]
    for cid in base_data.cids:
        if cid:
            base_entity.categories.append(get_category(int(cid)))

    if id == -1:
        base_entity.model = model
        entity.entity = base_entity
        web.ctx.orm.add(base_entity)
        web.ctx.orm.add(entity)
    else:
        web.ctx.orm.flush()

def del_entity(model, id):
    entity = get_entity(model, id)
    web.ctx.orm.delete(entity)

def get_entitys_category_ancestors(entity):
    return get_category_ancestors(entity.categories[0])

#def get_latest_entities(mname, cid, count):
#    model = get_model_by_name(mname)
#    return get_entities(model, cid, count)

def get_latest_entities(mname, cid, count):
    model = get_model_by_name(mname)
    return get_entities(model, cid, count)

