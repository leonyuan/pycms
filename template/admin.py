#encoding=utf-8
import web

from pycms.utils.admin import admin_login_required
from pycms.template.admin_form import template_form
from pycms.template.util import admin_render
from pycms.template.db import get_templates, save_template, get_template, del_template


class template_index:
    @admin_login_required
    def GET(self):
        templates = get_templates()
        req = web.ctx.req
        req.update({
            'templates': templates,
            })
        return admin_render.template_index(**req)

class template_add:
    @admin_login_required
    def GET(self):
        form = template_form()
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return admin_render.template_edit(**req)

    @admin_login_required
    def POST(self):
        form = template_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return admin_render.template_edit(**req)
        save_template(-1, form.d)
        raise web.seeother('/template/index')

class template_edit:
    @admin_login_required
    def GET(self, id):
        form = template_form()
        template = get_template(id)
        form.fill(template)
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return admin_render.template_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = template_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return admin_render.template_edit(**req)
        save_template(int(id), form.d)
        raise web.seeother('/template/index')

class template_delete:
    @admin_login_required
    def GET(self, id):
        del_template(id)
        raise web.seeother('/template/index')


urls = (
        '/template/index', template_index,
        '/template/add', template_add,
        '/template/(\d+)/edit', template_edit,
        '/template/(\d+)/delete', template_delete,
)
