import web
from blog.dbutil import new_article, get_articles, get_article, save_article, del_article, get_articles_category_ancestors
from blog.util import render
from common.util import login_required
from blog.form import article_form


class new:
    @login_required
    def GET(self):
        form = article_form()
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.new(**req)

    @login_required
    def POST(self):
        form = article_form()
        if not form.validates():
            return render.new(form=form)
        new_article(form.d.title, form.d.content)
        raise web.seeother('/')

class edit:
    @login_required
    def GET(self, id):
        form = article_form()
        article = get_article(id)
        form.fill(article)
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.new(**req)

    @login_required
    def POST(self, id):
        form = article_form()
        if not form.validates():
            return render.new(form=form)
        save_article(int(id), form.d.title, form.d.content)
        raise web.seeother('/')

class delete:
    @login_required
    def GET(self, id):
        del_article(id)
        raise web.seeother('/')

class index:
    def GET(self):
        """ Show page """
        articles = get_articles()
        req = web.ctx.req
        req.update({
            'articles': articles,
            })
        return render.index(**req)

class get:
    def GET(self, id):
        article = get_article(id)
        category_ancestors = get_articles_category_ancestors(article)
        req = web.ctx.req
        req.update({
            'article': article,
            'category_ancestors': category_ancestors,
            })
        return render.display(**req)

