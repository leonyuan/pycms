#encoding=utf-8
import web
from admin.util import render, admin_login_required
from blog.dbutil import get_category, get_categories, category_tree, get_templates, save_category, del_category
from admin.form import category_form


class admin:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        return render.article_admin(**req)

class index:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        req.update({
            'articles': [],
            })
        return render.article_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = category_form()
        templates = get_templates()
        categories = category_tree(None)
        parent_id = web.input(parent_id=None).parent_id
        form.parent_id.set_value(parent_id)
        req = web.ctx.req
        req.update({
            'form': form,
            'templates': templates,
            'categories': categories,
            })
        return render.category_edit(**req)

    @admin_login_required
    def POST(self):
        form = category_form()
        if not form.validates():
            templates = get_templates()
            categories = category_tree(None)
            req = web.ctx.req
            req.update({
                'form': form,
                'templates': templates,
                'categories': categories,
                })
            return render.category_edit(**req)
        save_category(-1, form.d)
        raise web.seeother('/category/index')

class edit:
    @admin_login_required
    def GET(self, id):
        form = category_form()
        category = get_category(id)
        templates = get_templates()
        categories = category_tree(None)
        form.fill(category)
        req = web.ctx.req
        req.update({
            'form': form,
            'templates': templates,
            'categories': categories,
            })
        return render.category_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = category_form()
        if not form.validates():
            return render.category_edit(form=form)
        save_category(int(id), form.d)
        raise web.seeother('/category/index')

class delete:
    @admin_login_required
    def GET(self, id):
        del_category(id)
        raise web.seeother('/category/index')


