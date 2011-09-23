import web
from admin import view, template, category, article

urls = (
        '', 'reindex',
        '/', view.index,
        '/login', view.login,
        '/logout', view.logout,
        '/submenu', view.submenu,
        '/curpos', view.curpos,
        '/template/index', template.index,
        '/template/add', template.add,
        '/template/edit/(\d+)', template.edit,
        '/template/delete/(\d+)', template.delete,
        '/category/index', category.index,
        '/category/add', category.add,
        '/category/edit/(\d+)', category.edit,
        '/category/delete/(\d+)', category.delete,
        '/category_tree', category.tree,
        '/article/admin', article.admin,
        '/article/index', article.index,
        '/article/add', article.add,
        '/article/edit/(\d+)', article.edit,
)


class reindex:
    def GET(self): raise web.seeother('/')

app_admin = web.application(urls, locals())
