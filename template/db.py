#encoding=utf-8
import web

from pycms.template.model import *
from pycms.db.util import populate


#-------------------------------
# template persistent method
#-------------------------------
def get_templates():
    return web.ctx.orm.query(Template).all()

def get_template(id):
    return web.ctx.orm.query(Template).get(id)

def save_template(id, data):
    if id == -1:
        template = Template()
    else:
        template = get_template(id)

    populate(template, data, Template)

    if id == -1:
        web.ctx.orm.add(template)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_template(id):
    template = get_template(id)
    web.ctx.orm.delete(template)
    web.ctx.orm.commit()

