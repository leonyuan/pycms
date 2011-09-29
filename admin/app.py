import web
from admin import view, model, field, template, category, article

urls = (
        '', 'reindex',
        '/', view.index,
        '/login', view.login,
        '/logout', view.logout,
        '/submenu', view.submenu,
        '/curpos', view.curpos,

        '/model/index', model.index,
        '/model/add', model.add,
        '/model/(\d+)/edit', model.edit,
        '/model/(\d+)/delete', model.delete,
        '/model/(\d+)/create_table', model.create_table,
        '/model/(\d+)/drop_table', model.drop_table,

        '/field/index', field.index,
        '/field/add', field.add,
        '/field/(\d+)/edit', field.edit,
        '/field/(\d+)/delete', field.delete,

        '/template/index', template.index,
        '/template/add', template.add,
        '/template/(\d+)/edit', template.edit,
        '/template/(\d+)/delete', template.delete,

        '/category/index', category.index,
        '/category/add', category.add,
        '/category/(\d+)/edit', category.edit,
        '/category/(\d+)/delete', category.delete,
        '/category_tree', category.tree,

        '/article/admin', article.admin,
        '/article/index', article.index,
        '/article/add', article.add,
        '/article/(\d+)/edit', article.edit,
)


class reindex:
    def GET(self): raise web.seeother('/')

app_admin = web.application(urls, locals())
