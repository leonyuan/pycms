#encoding=utf-8
import web
from admin.util import render, admin_login_required
from models.dbutil import get_model, get_active_models, get_relations, save_relation, get_relation, del_relation
from admin.form import relation_form


class index:
    @admin_login_required
    def GET(self):
        data = web.input()
        mid = data.mid
        relations = get_relations(mid)
        req = web.ctx.req
        req.update({
            'relations': relations,
            'mid': mid,
            })
        return render.relation_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = relation_form()
        data = web.input()
        mid = data.mid
        model = get_model(mid)
        models = get_active_models()
        req = web.ctx.req
        req.update({
            'models': models,
            'form': form,
            'mid': mid,
            'mtitle': model.title,
            })
        return render.relation_edit(**req)

    @admin_login_required
    def POST(self):
        form = relation_form()
        data = web.input()
        mid = data.mid
        if not form.validates():
            model = get_model(mid)
            models = get_active_models()
            req = web.ctx.req
            req.update({
                'models': models,
                'form': form,
                'mid': mid,
                'mtitle': model.title,
                })
            return render.relation_edit(**req)
        form_data = form.d
        form_data.model_id = mid
        save_relation(-1, form_data)
        raise web.seeother('/model/%s/edit' % mid)

class edit:
    @admin_login_required
    def GET(self, id):
        form = relation_form()
        relation = get_relation(id)
        form.fill(relation)
        data = web.input()
        models = get_active_models()
        mid = data.mid
        model = get_model(mid)
        req = web.ctx.req
        req.update({
            'models': models,
            'form': form,
            'mid': mid,
            'mtitle': model.title,
            })
        return render.relation_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = relation_form()
        data = web.input()
        mid = data.mid
        if not form.validates():
            model = get_model(mid)
            models = get_active_models()
            req = web.ctx.req
            req.update({
                'form': form,
                'models': models,
                'mid': mid,
                'mtitle': model.title,
                })
            return render.relation_edit(**req)
        save_relation(int(id), form.d)
        raise web.seeother('/model/%s/edit' % mid)

class delete:
    @admin_login_required
    def GET(self, id):
        del_relation(id)
        data = web.input()
        mid = data.mid
        raise web.seeother('/model/%s/edit' % mid)

