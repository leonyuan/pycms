#encoding=utf-8
import web
from admin.util import render, admin_login_required
from basis.dbutil import get_category
from models.dbutil import get_model_by_name, get_entities, new_entity, get_entity, save_entity, del_entity
from admin.form import entity_form
from datetime import datetime


class admin:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        return render.entity_admin(**req)

class index:
    @admin_login_required
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
        return render.entity_index(**req)

class add:
    @admin_login_required
    def GET(self, mname):
        model = get_model_by_name(mname)
        form = entity_form(mname)
        data = web.input()
        cid = data.cid
        catname = get_category(cid).name
        req = web.ctx.req
        req.update({
            'form': form,
            'cid': cid,
            'catname': catname,
            'mname': mname,
            'mtitle': model.title,
            'model': model,
            })
        return render.entity_edit(**req)

    @admin_login_required
    def POST(self, mname):
        form = entity_form(mname)
        data = web.input()
        cid = data.cid
        model = get_model_by_name(mname)
        if not form.validates():
            catname = get_category(cid).name
            req = web.ctx.req
            req.update({
                'form': form,
                'cid': cid,
                'catname': catname,
                'mname': mname,
                'mtitle': model.title,
            })
            return render.entity_edit(**req)
        form_data = form.d
        form_data.user_id = web.ctx.session._userid
        form_data.cid = cid
        new_entity(model, form_data)
        raise web.seeother('/%s/index?cid=%s' % (mname, cid))

class edit:
    @admin_login_required
    def GET(self, mname, id):
        model = get_model_by_name(mname)
        form = entity_form(mname)
        entity = get_entity(model, id)
        form.fill(entity)
        data = web.input()
        cid = data.cid
        catname = get_category(cid).name
        req = web.ctx.req
        req.update({
            'form': form,
            'cid': cid,
            'catname': catname,
            'mname': mname,
            'mtitle': model.title,
        })
        return render.entity_edit(**req)

    @admin_login_required
    def POST(self, mname, id):
        model = get_model_by_name(mname)
        form = entity_form(mname)
        data = web.input()
        cid = data.cid
        if not form.validates():
            catname = get_category(cid).name
            req = web.ctx.req
            req.update({
                'form': form,
                'cid': cid,
                'catname': catname,
                'mname': mname,
                'mtitle': model.title,
            })
            return render.entity_edit(**req)
        form_data = form.d
        form_data.user_id = web.ctx.session._userid
        form_data.cid = cid
        form_data.updated_time = datetime.now()
        save_entity(model, int(id), form_data)
        raise web.seeother('/%s/index?cid=%s' % (mname, cid))

class delete:
    @admin_login_required
    def GET(self, mname, id):
        model = get_model_by_name(mname)
        del_entity(model, id)
        data = web.input()
        cid = data.cid
        raise web.seeother('/%s/index?cid=%s' % (mname, cid))


