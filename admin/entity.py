#encoding=utf-8
import web
from admin.util import render, admin_login_required
from basis.dbutil import get_category, get_entities as get_base_entities, get_entity as get_base_entity
from models.dbutil import get_models, get_model_by_name, get_entities, new_entity, get_entity, save_entity, del_entity
from admin.form import base_entity_form, entity_form
from datetime import datetime

class admin:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        return render.entity_admin(**req)

class index:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        models = get_models()
        data = web.input()
        entities = get_base_entities()
        req.update({
            'entities': entities,
            'models': models,
            })
        return render.entity_index(**req)

class add:
    @admin_login_required
    def GET(self, mname):
        model = get_model_by_name(mname)
        base_form = base_entity_form()
        form = entity_form(mname)
        req = web.ctx.req
        req.update({
            'base_form': base_form,
            'form': form,
            'mname': mname,
            'mtitle': model.title,
            'model': model,
            })
        return render.entity_edit(**req)

    @admin_login_required
    def POST(self, mname):
        base_form = base_entity_form()
        form = entity_form(mname)
        model = get_model_by_name(mname)
        bv = base_form.validates()
        v = form.validates()
        if not bv or not v:
            req = web.ctx.req
            req.update({
                'base_form': base_form,
                'form': form,
                'mname': mname,
                'mtitle': model.title,
            })
            return render.entity_edit(**req)
        base_form_data = base_form.d
        base_form_data.user_id = web.ctx.session._userid
        form_data = form.d
        new_entity(model, base_form_data, form_data)
        raise web.seeother('/entity/index')

class edit:
    @admin_login_required
    def GET(self, id):
        base_entity = get_base_entity(id)
        model = base_entity.model
        base_form = base_entity_form()
        form = entity_form(model.name)
        entity = getattr(base_entity, model.name)
        base_form.fill(base_entity)
        form.fill(entity)
        data = web.input()
        req = web.ctx.req
        req.update({
            'base_form': base_form,
            'form': form,
            'mname': model.name,
            'mtitle': model.title,
        })
        return render.entity_edit(**req)

    @admin_login_required
    def POST(self, id):
        base_entity = get_base_entity(id)
        model = base_entity.model
        base_form = base_entity_form()
        form = entity_form(model.name)
        data = web.input()
        bv = base_form.validates()
        v = form.validates()
        if not bv or not v:
            req = web.ctx.req
            req.update({
                'base_form': base_form,
                'form': form,
                'mname': model.name,
                'mtitle': model.title,
            })
            return render.entity_edit(**req)
        base_form_data = base_form.d
        base_form_data.updated_time = datetime.now()
        form_data = form.d
        save_entity(model, int(id), base_form_data, form_data)
        raise web.seeother('/entity/index')

class delete:
    @admin_login_required
    def GET(self, id):
        base_entity = get_base_entity(id)
        model = base_entity.model
        entity = getattr(base_entity, model.name)
        if entity is not None:
            web.ctx.orm.delete(entity)
        if base_entity is not None:
            web.ctx.orm.delete(base_entity)
        raise web.seeother('/entity/index')


