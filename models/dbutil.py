#encoding=utf-8
import web
from sqlalchemy import func
from models.model import *
from common.dbutil import populate

#-------------------------------
# some utility
#-------------------------------

#-------------------------------
# model persistent method
#-------------------------------
def get_models():
    return web.ctx.orm.query(Model).all()

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

