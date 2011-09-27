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

