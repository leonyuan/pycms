#encoding=utf-8
import web
from admin.util import render, admin_login_required
from basis.dbutil import get_templates, save_template, get_template, del_template
from admin.form import template_form


class index:
    @admin_login_required
    def GET(self):
        templates = get_templates()
        req = web.ctx.req
        req.update({
            'templates': templates,
            })
        return render.template_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = template_form()
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.template_edit(**req)

    @admin_login_required
    def POST(self):
        form = template_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return render.template_edit(**req)
        save_template(-1, form.d)
        raise web.seeother('/template/index')

class edit:
    @admin_login_required
    def GET(self, id):
        form = template_form()
        template = get_template(id)
        form.fill(template)
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.template_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = template_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return render.template_edit(**req)
        save_template(int(id), form.d)
        raise web.seeother('/template/index')

class delete:
    @admin_login_required
    def GET(self, id):
        del_template(id)
        raise web.seeother('/template/index')


