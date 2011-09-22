#encoding=utf-8
import web
from common import render
from account.auth import is_logined, authenticate, login as auth_login, logout as auth_logout,\
        ERRCODE_USER_NOTEXISTS, ERRCODE_OK, ERRCODE_PASSWORD_NOTCORRECT
from account.dbutil import new_user
from account.form import login_form


class signup:
    def GET(self):
        if is_logined():
            raise web.seeother('/')
        return render.signup()

    def POST(self):
        data = web.input()
        new_user(data.username, data.password, data.email)
        raise web.seeother('/')

class login:
    def GET(self):
        if is_logined():
            raise web.seeother('/')
        redirect_url = ""
        data = web.input()
        if 'redirect_to' in data:
            redirect_url = data.redirect_to
        form = login_form()
        req = web.ctx.req
        req.update({
            'form': form,
            'redirect_url': redirect_url,
            })
        return render.login(**req)

    def POST(self):
        form = login_form()
        if not form.validates():
            return render.login(form=form)
        data = web.input()
        errcode, user = authenticate(data.username, data.password)
        req = web.ctx.req
        if errcode != ERRCODE_OK:
            if errcode == ERRCODE_USER_NOTEXISTS:
                req.err(u'用户未注册')
            elif errcode == ERRCODE_PASSWORD_NOTCORRECT:
                req.err(u'密码错误')

            if 'redirect_to' in data:
                redirect_url = data.redirect_to
            req.update({
                'form': form,
                'redirect_url': redirect_url,
                })
            return render.login(**req)
        auth_login(user)
        redirect_url = data.redirect_to
        if redirect_url:
            raise web.seeother(redirect_url)
        else:
            raise web.seeother('/', True)

class logout:
    def GET(self):
        auth_logout()
        raise web.seeother('/', True)

class reset:
    def GET(self):
        session.login = 0
        session.privilege = 0
        render = create_render(session.privilege)
        return "%s" % (render.logout())
