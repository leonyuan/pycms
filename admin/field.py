#encoding=utf-8
import web
from admin.util import render, admin_login_required
from models.dbutil import get_fields, save_field, get_field, del_field
from admin.form import field_form


class index:
    @admin_login_required
    def GET(self):
        data = web.input()
        mid = data.mid
        fields = get_fields(mid)
        req = web.ctx.req
        req.update({
            'fields': fields,
            'mid': mid,
            })
        return render.field_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = field_form()
        data = web.input()
        mid = data.mid
        req = web.ctx.req
        req.update({
            'form': form,
            'mid': mid,
            })
        return render.field_edit(**req)

    @admin_login_required
    def POST(self):
        form = field_form()
        data = web.input()
        mid = data.mid
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                'mid': mid,
                })
            return render.field_edit(**req)
        form_data = form.d
        form_data.model_id = mid
        save_field(-1, form_data)
        raise web.seeother('/model/%s/edit' % mid)

class edit:
    @admin_login_required
    def GET(self, id):
        form = field_form()
        field = get_field(id)
        form.fill(field)
        data = web.input()
        mid = data.mid
        req = web.ctx.req
        req.update({
            'form': form,
            'mid': mid,
            })
        return render.field_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = field_form()
        data = web.input()
        mid = data.mid
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                'mid': mid,
                })
            return render.field_edit(**req)
        save_field(int(id), form.d)
        raise web.seeother('/model/%s/edit' % mid)

class delete:
    @admin_login_required
    def GET(self, id):
        del_field(id)
        data = web.input()
        mid = data.mid
        raise web.seeother('/model/%s/edit' % mid)

