#encoding=utf-8
import web

from pycms.file.model import *
from pycms.db.util import populate


#-------------------------------
# file persistent method
#-------------------------------
def get_files():
    return web.ctx.orm.query(file).all()

def get_file(id):
    return web.ctx.orm.query(file).get(id)

def save_file(id, data):
    if id == -1:
        file = file()
    else:
        file = get_file(id)

    populate(file, data, file)

    if id == -1:
        web.ctx.orm.add(file)
    else:
        web.ctx.orm.flush()

def del_file(id):
    file = get_file(id)
    web.ctx.orm.delete(file)

