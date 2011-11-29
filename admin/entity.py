#encoding=utf-8
import web
from admin.util import render, admin_login_required
from basis.dbutil import get_category, category_tree, get_entities as get_base_entities, get_entity as get_base_entity
from models.dbutil import get_active_models, get_model_by_name, get_entities, new_entity, get_entity, save_entity, del_entity
from admin.form import base_entity_form, entity_form
from datetime import datetime
from common.util import Pagination
from basis.model import Entity
from common.widget import MyCheckboxGroup


class admin:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        return render.entity_admin(**req)

class index:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        models = get_active_models()
        data = web.input(p=1)
        pagination = Pagination(Entity, data.p)
        entities = pagination.queryset
        req.update({
            'entities': entities,
            'models': models,
            'pagination': pagination,
            })
        return render.entity_index(**req)

class add:
    @admin_login_required
    def GET(self, mname):
        model = get_model_by_name(mname)
        base_form = base_entity_form()
        form = entity_form(mname)
        categories = category_tree()
        req = web.ctx.req
        req.update({
            'base_form': base_form,
            'form': form,
            'mname': mname,
            'mtitle': model.title,
            'model': model,
            'categories': categories,
            })
        return render.entity_edit(**req)

    @admin_login_required
    def POST(self, mname):
        data = web.input(cids=[])
        base_form = base_entity_form()
        form = entity_form(mname)
        model = get_model_by_name(mname)
        bv = base_form.validates()
        v = form.validates()
        if not bv or not v:
            categories = category_tree()
            base_form.cids.set_value(data.cids)

            # populate multi value field
            pd = {}
            for item in form.inputs:
                if isinstance(item, MyCheckboxGroup):
                    pd[item.name] = []
            pdata = web.input(**pd)
            for k in pd.keys():
                getattr(form, k).set_value(getattr(pdata, k))

            req = web.ctx.req
            req.update({
                'base_form': base_form,
                'form': form,
                'mname': mname,
                'mtitle': model.title,
                'categories': categories,
            })
            return render.entity_edit(**req)

        base_form_data = base_form.d
        base_form_data.cids = data.cids
        base_form_data.user_id = web.ctx.session._userid
        form_data = form.d
        # populate multi value field
        pd = {}
        for item in form.inputs:
            if isinstance(item, MyCheckboxGroup):
                pd[item.name] = []
        pdata = web.input(**pd)
        for k in pd.keys():
            setattr(form_data, k, str(getattr(pdata, k)))

        new_entity(model, base_form_data, form_data)
        raise web.seeother('/entity/index')

class edit:
    @admin_login_required
    def GET(self, id):
        base_entity = get_base_entity(id)
        cids = [cate.id for cate in base_entity.categories]
        model = base_entity.model
        base_form = base_entity_form()
        base_form.cids.set_value(cids)
        form = entity_form(model.name)
        entity = getattr(base_entity, model.name)
        base_form.fill(base_entity)
        base_form.cids.value = cids
        form.fill(entity)
        # populate multi value field
        pd = []
        for item in form.inputs:
            if isinstance(item, MyCheckboxGroup):
                pd.append(item.name)
        for k in pd:
            getattr(form, k).set_value(eval(getattr(entity, k)))

        categories = category_tree()
        data = web.input()
        req = web.ctx.req
        req.update({
            'base_form': base_form,
            'form': form,
            'mname': model.name,
            'mtitle': model.title,
            'categories': categories,
        })
        return render.entity_edit(**req)

    @admin_login_required
    def POST(self, id):
        base_entity = get_base_entity(id)
        model = base_entity.model
        base_form = base_entity_form()
        form = entity_form(model.name)
        data = web.input(cids=[])
        bv = base_form.validates()
        v = form.validates()
        if not bv or not v:
            categories = category_tree()
            base_form.cids.set_value(data.cids)
            # populate multi value field
            pd = {}
            for item in form.inputs:
                if isinstance(item, MyCheckboxGroup):
                    pd[item.name] = []
            pdata = web.input(**pd)
            for k in pd.keys():
                getattr(form, k).set_value(getattr(pdata, k))

            req = web.ctx.req
            req.update({
                'base_form': base_form,
                'form': form,
                'mname': model.name,
                'mtitle': model.title,
                'categories': categories,
            })
            return render.entity_edit(**req)
        base_form_data = base_form.d
        base_form_data.cids = data.cids
        base_form_data.updated_time = datetime.now()
        form_data = form.d
        # populate multi value field
        pd = {}
        for item in form.inputs:
            if isinstance(item, MyCheckboxGroup):
                pd[item.name] = []
        pdata = web.input(**pd)
        for k in pd.keys():
            setattr(form_data, k, str(getattr(pdata, k)))

        save_entity(model, int(id), base_form_data, form_data)
        raise web.seeother('/entity/index')

class delete:
    @admin_login_required
    def GET(self, id):
        base_entity = get_base_entity(id)
        model = base_entity.model
        entity = getattr(base_entity, model.name)
        if entity is not None:
            web.ctx.orm.delete(entity)
        if base_entity is not None:
            web.ctx.orm.delete(base_entity)
        raise web.seeother('/entity/index')


