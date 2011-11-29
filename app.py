#!/bin/env python
'''
This file is main application file. It includes some things, database and session and hook, etc.
A significant hook is defined,  The hook defines some http request scope object to used in template files.
'''

import web
from common import load_sqla
from common.config import *
from common.util import context, yesorno
from common import view
from account import profile
from account.util import LazyUser
from admin.app import app_admin
from basis import entity
from models.util import init_model_class


web.config.debug = debug

urls = (
    '', view.reindex,
    '/', view.index,
    '/signup', profile.signup,
    '/login', profile.login,
    '/logout', profile.logout,

    '/admin', app_admin,

    '/(.+)/(\d+)', entity.get,
)

app = web.application(urls, globals())
db = web.database(dbn=db_engine, user=db_user, pw=db_password, db=db_name)
store = web.session.DBStore(db, session_tablename)

if web.config.get('_session') is None:
    session = web.session.Session(app, store, initializer={'_userid': -1})
    web.config._session = session
else:
    session = web.config._session

def session_hook():
    web.ctx.session = session

def request_hook():
    req = context()
    req['static_url'] = callable(static_url) and static_url() or static_url
    req['admin_url'] = web.ctx.homepath + '/admin'
    req['_userid'] = web.ctx.session._userid
    req['_s'] = web.net.websafe
    req['_yn'] = yesorno
    req['_uq'] = web.net.urlquote
    action = web.ctx.path.split('/')[-1]
    if action.find('_'):
        action = action.split('_')[-1]
    req['_ac'] = action
    web.ctx.__class__.user = LazyUser()
    req['_user'] = web.ctx.user
    web.ctx.req = req

app.add_processor(load_sqla)
app.add_processor(web.loadhook(session_hook))
app.add_processor(web.loadhook(request_hook))

# some system initiate activities
init_model_class()

if __name__ == '__main__':
    app.run()

