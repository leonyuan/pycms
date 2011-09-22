import web
from account.dbutil import get_perms_by_pid, get_nested_perms_by_pid, get_perm_namepath


def get_menus(parent):
    return get_perms_by_pid(parent)

def get_nested_menus(parent):
    return get_nested_perms_by_pid(parent)

def get_menu_namepath(menuid):
    return get_perm_namepath(menuid)

