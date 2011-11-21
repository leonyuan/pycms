#encoding=utf-8
import os
import os.path
import web
from admin.util import render, admin_login_required
from common import render as front_render
from common.config import publish_dir


class index:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        return render.publish_index(**req)

class homepage:
    @admin_login_required
    def GET(self):
        from common.view import index as app_index
        app_index_obj = app_index()
        html = app_index_obj.GET()
        path = os.path.join(publish_dir, 'index.html')
        try:
            f = open(path, 'w')
            try:
                f.write(html)
            finally:
                f.close()
        except IOError, ioe:
            web.debug('====IOError:%s' % ioe)

        raise web.seeother('/publish/index')

class entities:
    @admin_login_required
    def GET(self):
        from basis.entity import get as entity_get
        from basis.dbutil import get_entities as get_base_entities, get_entity as get_base_entity
        base_entities = get_base_entities()

        obj = entity_get()
        for base_entity in base_entities:
            html = obj.GET('', base_entity.id)
            crtime = base_entity.created_time
            sub_path = reduce(os.path.join, [base_entity.model.name, str(crtime.year), str(crtime.month), str(crtime.day)])
            path = os.path.join(publish_dir, sub_path)
            if not os.path.exists(path):
                os.makedirs(os.path.abspath(path))
            path = os.path.join(path, '%d.html' % base_entity.id)
            try:
                f = open(path, 'w')
                try:
                    f.write(html)
                finally:
                    f.close()
            except IOError, ioe:
                web.debug('====IOError:%s' % ioe)

        raise web.seeother('/publish/index')
