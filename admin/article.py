#encoding=utf-8
import web
from admin.util import render, admin_login_required
from blog.dbutil import get_category, get_article, new_article, save_article, get_articles
from admin.form import article_form
#from common.dbutil import utcnow
from datetime import datetime


class admin:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        return render.article_admin(**req)

class index:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        data = web.input()
        catid = data.catid
        articles = get_articles(catid)
        req.update({
            'articles': articles,
            'catid': catid,
            })
        return render.article_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = article_form()
        data = web.input()
        catid = data.catid
        catname = get_category(catid).name
        req = web.ctx.req
        req.update({
            'form': form,
            'catid': catid,
            'catname': catname,
            })
        return render.article_edit(**req)

    @admin_login_required
    def POST(self):
        form = article_form()
        data = web.input()
        catid = data.catid
        if not form.validates():
            catname = get_category(catid).name
            req = web.ctx.req
            req.update({
                'form': form,
                'catid': catid,
                'catname': catname,
            })
            return render.article_edit(**req)
        form_data = form.d
        form_data.user_id = web.ctx.session._userid
        new_article(form_data)
        raise web.seeother('/article/index?catid=%s' % catid)

class edit:
    @admin_login_required
    def GET(self, id):
        form = article_form()
        article = get_article(id)
        form.fill(article)
        data = web.input()
        catid = data.catid
        catname = get_category(catid).name
        req = web.ctx.req
        req.update({
            'form': form,
            'catid': catid,
            'catname': catname,
        })
        return render.article_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = article_form()
        data = web.input()
        catid = data.catid
        if not form.validates():
            catname = get_category(catid).name
            req = web.ctx.req
            req.update({
                'form': form,
                'catid': catid,
                'catname': catname,
            })
            return render.article_edit(**req)
        form_data = form.d
        form_data.updated_time = datetime.now()
        save_article(int(id), form_data)
        raise web.seeother('/article/index?catid=%s' % catid)

class delete:
    @admin_login_required
    def GET(self, id):
        del_category(id)
        raise web.seeother('/category/index')


