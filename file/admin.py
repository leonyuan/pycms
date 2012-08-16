#encoding=utf-8
import web
import os

from pycms.utils.admin import admin_login_required
from pycms.file.util import admin_render
from pycms.file.model import File
from pycms.file.admin_form import file_form


class file_index:
    @admin_login_required
    def GET(self):
        fpath = web.input(fpath='').fpath
        fpath_dir = os.path.join(web.config.site_template_dir, fpath)
        files = os.listdir(fpath_dir)
        files = [(fpath,f,os.path.isfile(os.path.join(fpath_dir, f))) for f in files]
        req = web.ctx.req
        req.update({
            'files': files,
            })
        return admin_render.file_index(**req)

class file_open:
    @admin_login_required
    def GET(self):
        fn = web.input(fn='').fn
        if not fn:
            raise web.seeother('/file/index')

        site_template_dir = web.config.site_template_dir
        is_file = os.path.isfile(os.path.join(site_template_dir, fn))
        lines = None
        if is_file:
            # f = open(os.path.join(site_template_dir, fn), 'r')
            f = File(os.path.join(site_template_dir, fn))
            form = file_form()
            form.fill(f)
            req = web.ctx.req
            req.update({
                'form': form,
                })

            return admin_render.file_edit(**req)
        else:
            raise web.seeother('/file/index?fpath='+fn)

    @admin_login_required
    def POST(self):
        form = file_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return admin_render.file_edit(**req)
        save_file(-1, form.d)
        raise web.seeother('/file/index')

class file_edit:
    @admin_login_required
    def GET(self, id):
        form = file_form()
        file = get_file(id)
        form.fill(file)
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return admin_render.file_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = file_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return admin_render.file_edit(**req)
        save_file(int(id), form.d)
        raise web.seeother('/file/index')

class file_delete:
    @admin_login_required
    def GET(self, id):
        del_file(id)
        raise web.seeother('/file/index')


urls = (
        '/file/index', file_index,
        '/file/open', file_open,
        '/file/(\d+)/edit', file_edit,
        '/file/(\d+)/delete', file_delete,
)
