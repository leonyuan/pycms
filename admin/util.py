import web
from common.util import render_mako
from account.dbutil import get_user
from account.auth import is_logined, authenticate, login as auth_login, logout as auth_logout, get_logined_user
from common.config import template_dir


ERR_NOTSUPERUSER = 11

render = render_mako(
            directories=[template_dir+'admin/'],
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
        return ERR_NOTSUPERUSER, user
    return errcode, user

def admin_login_required(view_func):
    def __dec_func(viewobj, *args, **kwargs):
        if is_admin_logined():
            return view_func(viewobj, *args, **kwargs)
        else:
            raise web.seeother('/login')
    return __dec_func


