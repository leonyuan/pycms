#encoding=utf-8
import web
from common import render
from basis.dbutil import get_latest_entities


class index:
    def GET(self):
        req = web.ctx.req
        req['get_latest_entities'] = get_latest_entities
        return render.index(**req)

class reindex:
    def GET(self): raise web.seeother('/')


