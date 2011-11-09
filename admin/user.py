#encoding=utf-8
import web
from admin.util import render, admin_login_required
from account.dbutil import get_users, save_user, get_user_byid, del_user
from admin.form import user_form, editpwd_form


class index:
    @admin_login_required
    def GET(self):
        users = get_users()
        req = web.ctx.req
        req.update({
            'users': users,
            })
        return render.user_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = user_form()
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.user_edit(**req)

    @admin_login_required
    def POST(self):
        form = user_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return render.user_edit(**req)
        save_user(-1, form.d)
        raise web.seeother('/user/index')

class edit:
    @admin_login_required
    def GET(self, id):
        form = user_form()
        user = get_user_byid(id)
        form.fill(user)
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.user_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = user_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return render.user_edit(**req)
        save_user(int(id), form.d)
        raise web.seeother('/user/index')

class editpwd:
    @admin_login_required
    def GET(self, id):
        form = editpwd_form()
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.user_editpwd(**req)

    @admin_login_required
    def POST(self, id):
        form = editpwd_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return render.user_editpwd(**req)
        save_user(int(id), form.d)
        raise web.seeother('/user/index')

class delete:
    @admin_login_required
    def GET(self, id):
        del_user(id)
        raise web.seeother('/user/index')


