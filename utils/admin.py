import os.path
import web
from pycms.utils.render import render_mako
from pycms.account.auth import is_logined, authenticate, login as auth_login, logout as auth_logout, get_logined_user
from pycms.account.db import get_user, get_perms_by_pid, get_nested_perms_by_pid, get_perm_namepath

ERR_NOTSUPERUSER = 11

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

def get_menus(parent):
    return get_perms_by_pid(parent)

def get_nested_menus(parent):
    return get_nested_perms_by_pid(parent)

def get_menu_namepath(menuid):
    return get_perm_namepath(menuid)

