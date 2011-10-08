import web
from basis.util import render
from models.dbutil import get_model_by_name, get_entities, get_entity, get_entitys_category_ancestors


class index:
    def GET(self, mname):
        req = web.ctx.req
        data = web.input()
        cid = data.cid
        model = get_model_by_name(mname)
        entities = get_entities(model, cid)
        req.update({
            'entities': entities,
            'cid': cid,
            'mname': mname,
            'mtitle': model.title,
            })
        return render.index(**req)

class get:
    def GET(self, mname, id):
        model = get_model_by_name(mname)
        entity = get_entity(model, id)
        category_ancestors = get_entitys_category_ancestors(entity)
        req = web.ctx.req
        req.update({
            'entity': entity,
            'category_ancestors': category_ancestors,
            })
        template = model.template.display_file
        return render.render(template, **req)

