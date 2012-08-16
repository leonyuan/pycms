#encoding=utf-8
import web
from pycms.category.db import get_category, get_categories, category_tree, category_tree2,\
        category_tree3, new_category, save_category, del_category
from pycms.category.admin_form import category_form
from pycms.category.util import admin_render
from pycms.utils.admin import admin_login_required
from pycms.category.db import get_category_by_slug, get_other_categories
from pycms.template.db import get_templates


class category_index:
    @admin_login_required
    def GET(self):
        categories = category_tree3()
        req = web.ctx.req
        req.update({
            'categories': categories,
            })
        return admin_render.category_index(**req)

def catslug_unique(data):
    if data.id < 1:
        return get_category_by_slug(data.slug) is None
    else:
        return not get_other_categories(data.id, data.slug)

class category_add:
    @admin_login_required
    def GET(self):
        form = category_form()
        categories = category_tree()
        templates = get_templates()
        parent_id = web.input(parent_id=None).parent_id
        form.parent_id.set_value(parent_id)
        req = web.ctx.req
        req.update({
            'form': form,
            'categories': categories,
            'templates': templates,
            })
        return admin_render.category_edit(**req)

    @admin_login_required
    def POST(self):
        form = category_form()
        valid = form.validates()
        is_unique_slug = get_category_by_slug(form.d.slug) is None
        if not valid or not is_unique_slug:
            if not is_unique_slug:
                form.slug.note = u"%s已存在，请重新指定。" % (form.d.slug)
            categories = category_tree()
            templates = get_templates()
            req = web.ctx.req
            req.update({
                'form': form,
                'categories': categories,
                'templates': templates,
                })
            return admin_render.category_edit(**req)
        new_category(form.d)
        raise web.seeother('/category/index')

class category_edit:
    @admin_login_required
    def GET(self, id):
        form = category_form()
        category = get_category(id)
        categories = category_tree()
        templates = get_templates()
        form.fill(category)
        req = web.ctx.req
        req.update({
            'form': form,
            'categories': categories,
            'templates': templates,
            })
        return admin_render.category_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = category_form()
        valid = form.validates()
        is_unique_slug = not get_other_categories(int(id), form.d.slug)
        if not valid or not is_unique_slug:
            if not is_unique_slug:
                form.slug.note = u"%s已存在，请重新指定。" % (form.d.slug)
            categories = category_tree()
            templates = get_templates()
            req = web.ctx.req
            req.update({
                'form': form,
                'categories': categories,
                'templates': templates,
                })
            return admin_render.category_edit(**req)

        save_category(int(id), form.d)
        raise web.seeother('/category/index')

class category_delete:
    @admin_login_required
    def GET(self, id):
        del_category(id)
        raise web.seeother('/category/index')

class category_treeview:
    def GET(self):
        category_tree_html = category_tree2()
        req = web.ctx.req
        req.update({
            'category_tree_html': category_tree_html,
            })
        return admin_render.category_tree(**req)

urls = (
        '/category/index', category_index,
        '/category/add', category_add,
        '/category/(\d+)/edit', category_edit,
        '/category/(\d+)/delete', category_delete,
        '/category_tree', category_treeview,
)
