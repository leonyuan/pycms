#!/bin/env python
'''
This file is main application file. It includes some things, database and session and hook, etc.
A significant hook is defined,  The hook defines some http request scope object to used in template files.
'''

import web
from web.contrib.template import render_mako
from common import load_sqla, render
from common.config import *
from account import profile
from admin.app import app_admin
from blog.app import app_blog
from common.util import context
from blog.dbutil import get_latest_articles


web.config.debug = debug

urls = (
    '', 'reindex',
    '/', 'index',
    '/signup', profile.signup,
    '/login', profile.login,
    '/logout', profile.logout,

    '/admin', app_admin,
    '/blog', app_blog,
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
    req['static_url'] = web.ctx.homedomain + web.ctx.homepath + '/static'
    req['_userid'] = web.ctx.session._userid
    req['_s'] = web.net.websafe
    req['_uq'] = web.net.urlquote
    action = web.ctx.path.split('/')[-1]
    if action.find('_'):
        action = action.split('_')[-1]
    req['_ac'] = action
    web.ctx.req = req

app.add_processor(web.loadhook(session_hook))
app.add_processor(web.loadhook(request_hook))
app.add_processor(load_sqla)


class index:
    def GET(self):
        req = web.ctx.req
        req['get_latest_articles'] = get_latest_articles
        return render.index(**req)

class reindex:
    def GET(self): raise web.seeother('/')

if __name__ == '__main__':
    app.run()

