#encoding=utf-8
import web
from account.model import *


#-------------------------------
# permission persistent method
#-------------------------------
def get_perm(id):
    return web.ctx.orm.query(Permission).get(id)

def get_perm_namepath(id):
    perm = get_perm(id)
    namepath = []
    if perm.parent is not None:
        namepath.extend(get_perm_namepath(perm.parent.id))
    namepath.append(perm.name)
    return namepath

def get_perms_by_pid(pid):
    return web.ctx.orm.query(Permission).filter_by(parent_id=pid)

def get_nested_perms_by_pid(pid):
    if pid is None:
        return
    perms = get_perms_by_pid(pid)
    ret_perms = list(perms)
    for perm in perms:
        if len(perm.children) > 0:
            ret_perms.append(get_nested_perms_by_pid(perm.id))
    return ret_perms


#-------------------------------
# user persistent method
#-------------------------------
def new_user(username, password, email):
    user = User(username, email)
    user.set_password(password)
    web.ctx.orm.add(user)

def get_user(username):
    return web.ctx.orm.query(User).filter_by(username=username).first()

def get_user_by_id(id):
    return web.ctx.orm.query(User).get(id)


