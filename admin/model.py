#encoding=utf-8
import web
from admin.util import render, admin_login_required
from models.dbutil import get_models, save_model, get_model, del_model, activate_model, inactivate_model
from models.util import build_model, create_schema, drop_schema
from admin.form import model_form


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
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.model_edit(**req)

    @admin_login_required
    def POST(self):
        form = model_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return render.model_edit(**req)
        save_model(-1, form.d)
        raise web.seeother('/model/index')

class edit:
    @admin_login_required
    def GET(self, id):
        form = model_form()
        model = get_model(id)
        form.fill(model)
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.model_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = model_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
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

