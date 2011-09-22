from os.path import abspath, dirname, join

import web
from web.contrib.template import render_mako
from account.dbutil import get_user
from account.auth import is_logined, authenticate, login as auth_login, logout as auth_logout, get_logined_user


ERRCODE_NOTSUPERUSER = 11

curdir = abspath(dirname(__file__))

render = render_mako(
            directories=[join(curdir, '../templates/admin/')],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )

def is_admin_logined():
    if is_logined():
        user = get_logined_user()
        if user.is_superuser:
            return True
    return False


def admin_authenticate(username, password):
    errcode, user = authenticate(username, password)
    if user is not None and not user.is_superuser:
        return ERRCODE_NOTSUPERUSER, user
    return errcode, user

def admin_login_required(view_func):
    def __dec_func(viewobj, *args, **kwargs):
        if is_admin_logined():
            return view_func(viewobj, *args, **kwargs)
        else:
            raise web.seeother('/login')
    return __dec_func


