#encoding=utf-8
import web
from account.model import *
from common.dbutil import populate


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
def get_users():
    return web.ctx.orm.query(User).all()

def get_user(username):
    return web.ctx.orm.query(User).filter_by(username=username).first()

def get_user_byid(id):
    return web.ctx.orm.query(User).get(id)

def save_user(id, data):
    if id == -1:
        user = User()
        user.set_password('pycms');
    else:
        user = get_user_byid(id)

    populate(user, data, User)

    if hasattr(data, 'password') and data.password:
        user.set_password(data.password)

    if id == -1:
        web.ctx.orm.add(user)
    else:
        web.ctx.orm.flush()

def del_user(id):
    user = get_user_byid(id)
    web.ctx.orm.delete(user)

