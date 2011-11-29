#encoding=utf-8
import web
from admin.util import render, admin_login_required
from models.dbutil import get_models, save_model, get_model, del_model, activate_model,\
    inactivate_model, get_fields, get_relations
from models.util import build_model, create_schema, drop_schema
from admin.form import model_form, typetext
from basis.dbutil import get_templates


class index:
    @admin_login_required
    def GET(self):
        models = get_models()
        req = web.ctx.req
        req.update({
            'models': models,
            })
        return render.model_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = model_form()
        templates = get_templates()
        req = web.ctx.req
        req.update({
            'form': form,
            'templates': templates,
            'fields': [],
            'relations': [],
            })
        return render.model_edit(**req)

    @admin_login_required
    def POST(self):
        form = model_form()
        if not form.validates():
            templates = get_templates()
            req = web.ctx.req
            req.update({
                'form': form,
                'templates': templates,
                'fields': [],
                'relations': [],
                })
            return render.model_edit(**req)
        save_model(-1, form.d)
        raise web.seeother('/model/index')

class edit:
    @admin_login_required
    def GET(self, id):
        templates = get_templates()
        form = model_form()
        model = get_model(id)
        fields = get_fields(id)
        relations = get_relations(id)
        form.fill(model)
        req = web.ctx.req
        req.update({
            'mid': id,
            'form': form,
            'templates': templates,
            'fields': fields,
            'relations': relations,
            '_typetext': typetext,
            })
        return render.model_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = model_form()
        if not form.validates():
            templates = get_templates()
            fields = get_fields(id)
            relations = get_relations(id)
            req = web.ctx.req
            req.update({
                'mid': id,
                'form': form,
                'templates': templates,
                'fields': fields,
                'relations': relations,
                })
            return render.model_edit(**req)
        save_model(int(id), form.d)
        raise web.seeother('/model/index')

class delete:
    @admin_login_required
    def GET(self, id):
        del_model(id)
        raise web.seeother('/model/index')

class create_table:
    @admin_login_required
    def GET(self, id):
        model = get_model(id)
        create_schema(model)
        activate_model(model)
        raise web.seeother('/model/index')

class drop_table:
    @admin_login_required
    def GET(self, id):
        model = get_model(id)
        drop_schema(model)
        inactivate_model(model)
        raise web.seeother('/model/index')

