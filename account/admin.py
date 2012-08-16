#encoding=utf-8
import web
from pycms.account.util import admin_render
from pycms.utils.admin import admin_login_required
from pycms.account.db import *
from pycms.account.admin_form import user_form, editpwd_form, group_form


class user_index:
    @admin_login_required
    def GET(self):
        users = get_users()
        req = web.ctx.req
        req.update({
            'users': users,
            })
        return admin_render.user_index(**req)

class user_add:
    @admin_login_required
    def GET(self):
        form = user_form()
        groups = get_groups()
        req = web.ctx.req
        req.update({
            'form': form,
            'groups': groups,
            'user_groups': [],
            })
        return admin_render.user_edit(**req)

    @admin_login_required
    def POST(self):
        form = user_form()
        valid = form.validates()
        is_unique_username = get_user(form.username.get_value()) is None
        if not valid or not is_unique_username:
            if not is_unique_username:
                form.username.note = u"%s已存在，请重新指定。" % (form.username.get_value())
            groups = get_groups()
            req = web.ctx.req
            req.update({
                'form': form,
                'groups': groups,
                'user_groups': [],
                })
            return admin_render.user_edit(**req)
        data = web.input(groups=[])
        form_data = form.d
        form_data.gids = data.groups
        save_user(-1, form_data)
        raise web.seeother('/user/index')

class user_edit:
    @admin_login_required
    def GET(self, id):
        form = user_form()
        user = get_user_byid(id)
        form.fill(user)
        groups = get_groups()
        user_groups = user.groups
        req = web.ctx.req
        req.update({
            'uid': user.id,
            'form': form,
            'groups': groups,
            'user_groups': user_groups,
            })
        return admin_render.user_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = user_form()
        valid = form.validates()
        is_unique_username = not get_other_users(int(id), form.username.get_value())
        if not valid or not is_unique_username:
            if not is_unique_username:
                form.username.note = u"%s已存在，请重新指定。" % (form.username.get_value())
            groups = get_groups()
            user = get_user_byid(id)
            user_groups = user.groups
            req = web.ctx.req
            req.update({
                'uid': user.id,
                'form': form,
                'groups': groups,
                'user_groups': user_groups,
                })
            return admin_render.user_edit(**req)
        data = web.input(groups=[])
        form_data = form.d
        form_data.gids = data.groups
        save_user(int(id), form_data)
        raise web.seeother('/user/index')

class user_editpwd:
    @admin_login_required
    def GET(self, id):
        form = editpwd_form()
        req = web.ctx.req
        req.update({
            'form': form,
            })
        return admin_render.user_editpwd(**req)

    @admin_login_required
    def POST(self, id):
        form = editpwd_form()
        if not form.validates():
            req = web.ctx.req
            req.update({
                'form': form,
                })
            return admin_render.user_editpwd(**req)
        change_password(int(id), form.d)
        raise web.seeother('/user/index')

class user_delete:
    @admin_login_required
    def GET(self, id):
        del_user(id)
        raise web.seeother('/user/index')

class group_index:
    @admin_login_required
    def GET(self):
        groups = get_groups()
        req = web.ctx.req
        req.update({
            'groups': groups,
            })
        return admin_render.group_index(**req)

class group_add:
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
        return admin_render.group_edit(**req)

    @admin_login_required
    def POST(self):
        form = group_form()
        valid = form.validates()
        is_unique_name = get_group(form.name.get_value()) is None
        if not valid or not is_unique_name:
            if not is_unique_name:
                form.name.note = u"%s已存在，请重新指定。" % (form.name.get_value())
            users = get_users()
            req = web.ctx.req
            req.update({
                'form': form,
                'users': users,
                'group_users': [],
                })
            return admin_render.group_edit(**req)
        data = web.input(users=[])
        form_data = form.d
        form_data.uids = data.users
        save_group(-1, form_data)
        raise web.seeother('/group/index')

class group_edit:
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
        return admin_render.group_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = group_form()
        valid = form.validates()
        is_unique_name = not get_other_groups(int(id), form.name.get_value())
        if not valid or not is_unique_name:
            if not is_unique_name:
                form.name.note = u"%s已存在，请重新指定。" % (form.name.get_value())
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
            return admin_render.group_edit(**req)
        data = web.input(users=[])
        form_data = form.d
        form_data.uids = data.users
        save_group(int(id), form_data)
        raise web.seeother('/group/index')


class group_delete:
    @admin_login_required
    def GET(self, id):
        del_group(id)
        raise web.seeother('/group/index')

urls = (
        '/user/index', user_index,
        '/user/add', user_add,
        '/user/(\d+)/edit', user_edit,
        '/user/(\d+)/editpwd', user_editpwd,
        '/user/(\d+)/delete', user_delete,

        '/group/index', group_index,
        '/group/add', group_add,
        '/group/(\d+)/edit', group_edit,
        '/group/(\d+)/delete', group_delete,
)

