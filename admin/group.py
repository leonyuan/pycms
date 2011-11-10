#encoding=utf-8
import web
from admin.util import render, admin_login_required
from account.dbutil import get_users, get_groups, save_group, get_group_byid, del_group
from admin.form import group_form


class index:
    @admin_login_required
    def GET(self):
        groups = get_groups()
        req = web.ctx.req
        req.update({
            'groups': groups,
            })
        return render.group_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = group_form()
        users = get_users()
        req = web.ctx.req
        req.update({
            'form': form,
            'users': users,
            'group_users': [],
            })
        return render.group_edit(**req)

    @admin_login_required
    def POST(self):
        form = group_form()
        if not form.validates():
            users = get_users()
            req = web.ctx.req
            req.update({
                'form': form,
                'users': users,
                'group_users': [],
                })
            return render.group_edit(**req)
        data = web.input(users=[])
        form_data = form.d
        form_data.uids = data.users
        save_group(-1, form_data)
        raise web.seeother('/group/index')

class edit:
    @admin_login_required
    def GET(self, id):
        form = group_form()
        group = get_group_byid(id)
        form.fill(group)
        users = get_users()
        group_users = group.users
        req = web.ctx.req
        req.update({
            'form': form,
            'users': users,
            'group_users': group_users,
            })
        return render.group_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = group_form()
        if not form.validates():
            group = get_group_byid(id)
            form.fill(group)
            users = get_users()
            group_users = group.users
            req = web.ctx.req
            req.update({
                'form': form,
                'users': users,
                'group_users': group_users,
                })
            return render.group_edit(**req)
        data = web.input(users=[])
        form_data = form.d
        form_data.uids = data.users
        save_group(int(id), form_data)
        raise web.seeother('/group/index')


class delete:
    @admin_login_required
    def GET(self, id):
        del_group(id)
        raise web.seeother('/group/index')


