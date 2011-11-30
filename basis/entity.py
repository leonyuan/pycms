import web
from basis.util import render
from models.dbutil import get_model_by_name, get_entities, get_entity
from basis.dbutil import get_entity as get_base_entity, get_entitys_category_ancestors


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
        base_entity = get_base_entity(id)
        model = base_entity.model
        entity = getattr(base_entity, model.name)
        category_ancestors = get_entitys_category_ancestors(base_entity)
        req = web.ctx.req
        req[model.name] = entity
        req.update({
            'base_entity': base_entity,
            'entity': entity,
            'category_ancestors': category_ancestors,
            })
        template = model.template.display_file
        return render.render(template, **req)

