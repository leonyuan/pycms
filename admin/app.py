import web
from admin import view, model, field, relation, template, category, article, entity

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

        '/relation/index', relation.index,
        '/relation/add', relation.add,
        '/relation/(\d+)/edit', relation.edit,
        '/relation/(\d+)/delete', relation.delete,

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

        '/entity/admin', entity.admin,
        '/(.+)/index', entity.index,
        '/(.+)/add', entity.add,
        '/(.+)/(\d+)/edit', entity.edit,
        '/(.+)/(\d+)/delete', entity.delete,
)


class reindex:
    def GET(self): raise web.seeother('/')

app_admin = web.application(urls, locals())
