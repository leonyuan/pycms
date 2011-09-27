import web
from blog import article

urls = (
        '', 'reindex',
        '/', article.index,
        '/new', article.new,
        '/edit/(\d+)', article.edit,
        '/del/(\d+)', article.delete,
        '/(.*)', article.get
)

class reindex:
    def GET(self): raise web.seeother('/')

class blog:
    def GET(self, path):
        return 'blog ' + path

app_blog = web.application(urls, locals())
