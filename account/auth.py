import web
from account.dbutil import get_user, get_user_byid


ERRCODE_OK = 0
ERRCODE_USER_NOTEXISTS = 1
ERRCODE_PASSWORD_NOTCORRECT = 2
ERRCODE_NOTACTIVE = 3

def authenticate(username, password):
    user = get_user(username)
    if user is None:
        return ERRCODE_USER_NOTEXISTS, None
    if not user.is_active:
        return ERRCODE_NOTACTIVE, user
    if user.check_password(password):
        return ERRCODE_OK, user
    else:
        return ERRCODE_PASSWORD_NOTCORRECT, user

def login(user):
    if '_userid' in web.ctx.session:
        if web.ctx.session._userid != user.id:
            del web.ctx.session._userid
    web.ctx.session._userid = user.id
    web.ctx.user = user

def logout():
    web.ctx.session.kill()

def is_logined():
    return web.ctx.session._userid != -1

def get_logined_user():
    if is_logined():
        uid = web.ctx.session._userid
        return get_user_byid(uid)

