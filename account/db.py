#encoding=utf-8
import web
from sqlalchemy.orm import scoped_session, sessionmaker
from pycms.account.model import *
from pycms.db.util import populate, engine


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

def get_other_users(id, username):
    return web.ctx.orm.query(User).filter(User.username==username).filter(User.id!=id).all()

def get_user_byid(id):
    return web.ctx.orm.query(User).get(id)

def get_user_byid_with_alone_db_session(id):
    Session  = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
    session = Session()
    user = session.query(User).get(id)
    session.close()
    Session.remove()
    return user

def save_user(id, data):
    if id == -1:
        user = User()
        user.set_password(web.config.default_password);
    else:
        user = get_user_byid(id)

    populate(user, data, User)

    if hasattr(data, 'password') and data.password:
        user.set_password(data.password)

    for i in range(len(user.groups)-1,-1,-1):
        del user.groups[i]
    for gid in data.gids:
        user.groups.append(get_group_byid(int(gid)))

    if id == -1:
        web.ctx.orm.add(user)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_user(id):
    user = get_user_byid(id)
    web.ctx.orm.delete(user)
    web.ctx.orm.commit()

def change_password(id, data):
    user = get_user_byid(id)
    user.set_password(data.password)
    web.ctx.orm.flush()
    web.ctx.orm.commit()

#-------------------------------
# group persistent method
#-------------------------------
def get_groups():
    return web.ctx.orm.query(Group).all()

def get_group(name):
    return web.ctx.orm.query(Group).filter_by(name=name).first()

def get_group_byid(id):
    return web.ctx.orm.query(Group).get(id)

def get_other_groups(id, name):
    return web.ctx.orm.query(Group).filter(Group.name==name).filter(Group.id!=id).all()

def save_group(id, data):
    if id == -1:
        group = Group()
    else:
        group = get_group_byid(id)

    populate(group, data, Group)

    for i in range(len(group.users)-1,-1,-1):
        del group.users[i]
    for uid in data.uids:
        group.users.append(get_user_byid(int(uid)))

    if id == -1:
        web.ctx.orm.add(group)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_group(id):
    group = get_group_byid(id)
    web.ctx.orm.delete(group)
    web.ctx.orm.commit()

