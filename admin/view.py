#encoding=utf-8
import web
from account.auth import is_logined, authenticate, login as auth_login, logout as auth_logout,\
        ERRCODE_USER_NOTEXISTS, ERRCODE_OK, ERRCODE_PASSWORD_NOTCORRECT, ERRCODE_NOTACTIVE
from admin.util import is_admin_logined, admin_authenticate, render, ERRCODE_NOTSUPERUSER, admin_login_required
from admin.form import admin_login_form
from admin.menu import get_menus, get_menu_namepath

class index:
    @admin_login_required
    def GET(self):
        top_menus = get_menus(None)
        req = web.ctx.req
        req.update({
            'top_menus': top_menus,
            })
        return render.index(**req)

class login:
    def GET(self):
        if is_admin_logined():
            raise web.seeother('/')
        data = web.input()
        form = admin_login_form()
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return render.login(**req)

    def POST(self):
        form = admin_login_form()
        req = web.ctx.req
        if not form.validates():
            req.update({
                'form': form,
                })
            return render.login(**req)
        data = web.input()
        errcode, user = admin_authenticate(data.username, data.password)
        if errcode != ERRCODE_OK:
            if errcode == ERRCODE_USER_NOTEXISTS:
                form.username.note = u'用户未注册'
            elif errcode == ERRCODE_NOTACTIVE:
                form.username.note = u'用户未激活'
            elif errcode == ERRCODE_PASSWORD_NOTCORRECT:
                form.password.note = u'密码错误'
            elif errcode == ERRCODE_NOTSUPERUSER:
                form.username.note = u'不是管理员用户'

            req.update({
                'form': form,
                })
            return render.login(**req)

        auth_login(user)
        raise web.seeother('/')

class logout:
    def GET(self):
        auth_logout()
        raise web.seeother('/')

class submenu:
    @admin_login_required
    def POST(self):
        data = web.input()
        menus = get_menus(data.p)
        req = web.ctx.req
        req.update({
            'menus': menus,
            })
        return render.submenu(**req)

class curpos:
    @admin_login_required
    def GET(self):
        data = web.input()
        path = get_menu_namepath(data.menuid)
        return ' > '.join(path)

