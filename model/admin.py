#encoding=utf-8
from datetime import datetime
import web
from pycms.utils.admin import admin_login_required
from pycms.model.db import *
from pycms.model.util import build_model, create_schema, drop_schema, admin_render
from pycms.model.admin_form import *
from pycms.template.db import get_templates
from pycms.utils.paging import Pagination
from pycms.category.db import category_tree


#-------------------------------
# model views
#-------------------------------
class model_index:
    @admin_login_required
    def GET(self):
        models = get_models()
        req = web.ctx.req
        req.update({
            'models': models,
            })
        return admin_render.model_index(**req)

class model_add:
    @admin_login_required
    def GET(self):
        form = model_form()
        models = get_active_models()
        templates = get_templates()
        req = web.ctx.req
        req.update({
            'form': form,
            'templates': templates,
            'models': models,
            'fields': [],
            'relations': [],
            })
        return admin_render.model_edit(**req)

    @admin_login_required
    def POST(self):
        form = model_form()
        valid = form.validates()
        is_unique_name = get_model_by_name(form.name.get_value()) is None
        if not valid or not is_unique_name:
            if not is_unique_name:
                form.name.note = u"%s已存在，请重新指定。" % (form.name.get_value())
            templates = get_templates()
            models = get_active_models()
            req = web.ctx.req
            req.update({
                'form': form,
                'templates': templates,
                'models': models,
                'fields': [],
                'relations': [],
                })
            return admin_render.model_edit(**req)
        save_model(-1, form.d)
        raise web.seeother('/model/index')

class model_view:
    @admin_login_required
    def GET(self, id):
        form = model_form()
        model = get_model(id)
        fields = get_fields(id)
        relations = get_relations(id)
        form.fill(model)
        req = web.ctx.req
        req.update({
            'mid': id,
            'form': form,
            'model': model,
            'fields': fields,
            'relations': relations,
            '_typetext': typetext,
            })
        return admin_render.model_view(**req)

class model_edit:
    @admin_login_required
    def GET(self, id):
        model = get_model(id)
        if model.is_active:
            raise web.seeother('/model/%s/view' % id)
        templates = get_templates()
        models = get_active_models()
        form = model_form()
        fields = get_fields(id)
        relations = get_relations(id)
        form.fill(model)
        req = web.ctx.req
        req.update({
            'mid': id,
            'form': form,
            'templates': templates,
            'models': models,
            'fields': fields,
            'relations': relations,
            '_typetext': typetext,
            })
        return admin_render.model_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = model_form()
        valid = form.validates()
        is_unique_name = not get_other_models(int(id), form.name.get_value())
        if not valid or not is_unique_name:
            if not is_unique_name:
                form.name.note = u"%s已存在，请重新指定。" % (form.name.get_value())
            templates = get_templates()
            models = get_active_models()
            fields = get_fields(id)
            relations = get_relations(id)
            req = web.ctx.req
            req.update({
                'mid': id,
                'form': form,
                'templates': templates,
                'models': models,
                'fields': fields,
                'relations': relations,
                })
            return admin_render.model_edit(**req)
        save_model(int(id), form.d)
        raise web.seeother('/model/index')

class model_delete:
    @admin_login_required
    def GET(self, id):
        del_model(id)
        raise web.seeother('/model/index')

#-------------------------------
# field views
#-------------------------------
class field_index:
    @admin_login_required
    def GET(self):
        data = web.input()
        mid = data.mid
        fields = get_fields(mid)
        req = web.ctx.req
        req.update({
            'fields': fields,
            'mid': mid,
            })
        return admin_render.field_index(**req)

class field_add:
    @admin_login_required
    def GET(self):
        forms = {}
        for form_name, form_cls in FIELD_FORM_TYPE.items():
            forms[form_name] = form_cls()

        data = web.input()
        mid = data.mid
        model = get_model(mid)
        req = web.ctx.req
        req.update(forms)
        req.update({
            'mid': mid,
            'mtitle': model.title,
            'type': '__all__',
            })
        return admin_render.field_edit(**req)

    @admin_login_required
    def POST(self):
        data = web.input(options=[])
        form = FIELD_FORM_TYPE[data.type+'_form']()
        mid = data.mid
        if not form.validates():
            model = get_model(mid)
            if data.type == 'select' or data.type == 'radio' or data.type == 'checkbox':
                form.options.set_value(data.options)

            req = web.ctx.req
            req.update({
                'type': data.type,
                data.type+'_form': form,
                'mid': mid,
                'mtitle': model.title,
                })
            return admin_render.field_edit(**req)
        form_data = form.d
        form_data.type = data.type
        form_data.options = data.options
        form_data.model_id = mid
        save_field(-1, form_data)
        raise web.seeother('/model/%s/edit' % mid)

class field_view:
    @admin_login_required
    def GET(self, id):
        field = get_field(id)
        form = FIELD_FORM_TYPE[field.type+'_form']()
        form.fill(field)
        if field.props:
            prop_dict = eval(field.props)
            if field.type == 'text':
                form.lines.set_value(prop_dict['lines'])
                form.editor.set_value(prop_dict['editor'])
            elif field.type == 'select' or field.type == 'radio' or field.type == 'checkbox':
                form.options.set_value(prop_dict['options'])
                if field.type == 'select':
                    form.is_multisel.set_value(prop_dict['is_multisel'])

        data = web.input()
        mid = data.mid
        model = get_model(mid)
        req = web.ctx.req
        req.update({
            'type': field.type,
            field.type+'_form': form,
            'mid': mid,
            'mtitle': model.title,
            })
        return admin_render.field_view(**req)

class field_edit:
    @admin_login_required
    def GET(self, id):
        field = get_field(id)
        form = FIELD_FORM_TYPE[field.type+'_form']()
        form.fill(field)
        if field.props:
            prop_dict = eval(field.props)
            if field.type == 'text':
                form.lines.set_value(prop_dict['lines'])
                form.editor.set_value(prop_dict['editor'])
            elif field.type == 'select' or field.type == 'radio' or field.type == 'checkbox':
                form.options.set_value(prop_dict['options'])
                if field.type == 'select':
                    form.is_multisel.set_value(prop_dict['is_multisel'])

        data = web.input()
        mid = data.mid
        model = get_model(mid)
        req = web.ctx.req
        req.update({
            'type': field.type,
            field.type+'_form': form,
            'mid': mid,
            'mtitle': model.title,
            })
        return admin_render.field_edit(**req)

    @admin_login_required
    def POST(self, id):
        data = web.input(options=[])
        form = FIELD_FORM_TYPE[data.type+'_form']()
        mid = data.mid
        if not form.validates():
            model = get_model(mid)
            if data.type == 'select' or data.type == 'radio' or data.type == 'checkbox':
                form.options.set_value(data.options)
            req = web.ctx.req
            req.update({
                'type': data.type,
                data.type+'_form': form,
                'mid': mid,
                'mtitle': model.title,
                })
            return admin_render.field_edit(**req)
        form_data = form.d
        form_data.type = data.type
        form_data.options = data.options
        save_field(int(id), form_data)
        raise web.seeother('/model/%s/edit' % mid)

class field_delete:
    @admin_login_required
    def GET(self, id):
        del_field(id)
        data = web.input()
        mid = data.mid
        raise web.seeother('/model/%s/edit' % mid)

#-------------------------------
# relation views
#-------------------------------
class relation_index:
    @admin_login_required
    def GET(self):
        data = web.input()
        mid = data.mid
        relations = get_relations(mid)
        req = web.ctx.req
        req.update({
            'relations': relations,
            'mid': mid,
            })
        return admin_render.relation_index(**req)

class relation_add:
    @admin_login_required
    def GET(self):
        form = relation_form()
        data = web.input()
        mid = data.mid
        model = get_model(mid)
        models = get_active_models()
        req = web.ctx.req
        req.update({
            'models': models,
            'form': form,
            'mid': mid,
            'mtitle': model.title,
            })
        return admin_render.relation_edit(**req)

    @admin_login_required
    def POST(self):
        form = relation_form()
        data = web.input()
        mid = data.mid
        if not form.validates():
            model = get_model(mid)
            models = get_active_models()
            req = web.ctx.req
            req.update({
                'models': models,
                'form': form,
                'mid': mid,
                'mtitle': model.title,
                })
            return admin_render.relation_edit(**req)
        form_data = form.d
        form_data.model_id = mid
        save_relation(-1, form_data)
        raise web.seeother('/model/%s/edit' % mid)

class relation_edit:
    @admin_login_required
    def GET(self, id):
        form = relation_form()
        relation = get_relation(id)
        form.fill(relation)
        data = web.input()
        models = get_active_models()
        mid = data.mid
        model = get_model(mid)
        req = web.ctx.req
        req.update({
            'models': models,
            'form': form,
            'mid': mid,
            'mtitle': model.title,
            })
        return admin_render.relation_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = relation_form()
        data = web.input()
        mid = data.mid
        if not form.validates():
            model = get_model(mid)
            models = get_active_models()
            req = web.ctx.req
            req.update({
                'form': form,
                'models': models,
                'mid': mid,
                'mtitle': model.title,
                })
            return admin_render.relation_edit(**req)
        save_relation(int(id), form.d)
        raise web.seeother('/model/%s/edit' % mid)

class relation_delete:
    @admin_login_required
    def GET(self, id):
        del_relation(id)
        data = web.input()
        mid = data.mid
        raise web.seeother('/model/%s/edit' % mid)

#-------------------------------
# info views
#-------------------------------
class info_admin:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        return admin_render.info_admin(**req)

class info_index:
    @admin_login_required
    def GET(self):
        req = web.ctx.req
        models = get_top_models_with_entnum()
        req.update({
            'models': models,
            })
        return admin_render.info_index(**req)


class info_list:
    @admin_login_required
    def GET(self, mname):
        model = get_model_by_name(mname)
        req = web.ctx.req
        data = web.input(p=1, t='', c='')
        pagination = Pagination(info_record_query1(model, data.t, data.c), info_count_query1(model, data.t, data.c), data.p)
        qs = pagination.queryset
        entities = qs.all()
        eids = map(lambda row: row[0].id, entities)
        catents = catent_cname(eids)
        eids_of_model = query_eids_of_model(model)
        eids_of_model = map(lambda row: row[0], eids_of_model)
        curcats = cats_of_ents(eids_of_model)
        entities = [list(row) for row in entities]
        for ent in entities:
            ent.append([])

        for row in catents:
            for ent in entities: # entities content 0: Entity object, 1: model title, 2: username, 3: []
                if ent[0].id == row.entity_id:
                    ent[2].append(row.name)

        req.update({
            'entities': entities,
            'curcats': curcats,
            'model': model,
            'pagination': pagination,
            't': data.t,
            'c': data.c,
            })
        return admin_render.info_list(**req)

class info_add:
    @admin_login_required
    def GET(self, mname):
        model = get_model_by_name(mname)
        eform = entity_form()
        form = info_form(mname)
        submodels = model.children
        formset = {}
        if submodels:
            for submodel in submodels:
                forms = [info_form(submodel.name, '0'), info_form(submodel.name, '__prefix__')]
                subform = dict(prefix=submodel.name, title=submodel.title, forms=forms)
                formset.update({submodel.name: subform})
        categories = category_tree()
        req = web.ctx.req
        req.update({
            'eform': eform,
            'form': form,
            'formset': formset,
            'mname': mname,
            'mtitle': model.title,
            'model': model,
            'categories': categories,
            })
        return admin_render.info_edit(**req)

    @admin_login_required
    def POST(self, mname):
        data = web.input(cids=[])
        eform = entity_form()
        form = info_form(mname)
        model = get_model_by_name(mname)

        bv = eform.validates()
        v = form.validates()
        is_unique_slug = get_entity_by_slug(eform.slug.get_value()) is None

        submodels = model.children
        sfvs = []
        formset = {}
        if submodels:
            for submodel in submodels:
                forms_total = int(getattr(data, submodel.name+'-TOTAL_FORMS'))
                forms = []
                for i in range(forms_total):
                    subformobj = info_form(submodel.name, str(i))
                    sfv = subformobj.validates()
                    sfvs.append(sfv)
                    forms.append(subformobj)
                forms.append(info_form(submodel.name, '__prefix__'))
                subform = dict(prefix=submodel.name, title=submodel.title, forms=forms)
                formset.update({submodel.name: subform})

        sfsv = reduce(bool.__and__, sfvs) if sfvs else True

        if not bv or not v or not sfsv or not is_unique_slug:
            if not is_unique_slug:
                eform.slug.note = u"%s已存在，请重新指定。" % (eform.slug.get_value())
            categories = category_tree()
            eform.cids.set_value(data.cids)
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
                'eform': eform,
                'form': form,
                'formset': formset,
                'mname': mname,
                'mtitle': model.title,
                'categories': categories,
            })
            return admin_render.info_edit(**req)

        eform_data = eform.d
        eform_data.cids = data.cids
        eform_data.user_id = web.ctx.session._userid
        form_data = form.d

        sforms_data = {}
        if formset:
            for sform_name, subform in formset.items():
                formsnum = len(subform['forms'])
                for i, subformobj in enumerate(subform['forms']):
                    if i < formsnum-1:
                        sforms_data.setdefault(sform_name, []).append(subformobj.d)

        # populate multi value field
        pd = {}
        for item in form.inputs:
            if isinstance(item, MyCheckboxGroup):
                pd[item.name] = []
        pdata = web.input(**pd)
        for k in pd.keys():
            setattr(form_data, k, str(getattr(pdata, k)))

        new_info(model, eform_data, form_data, sforms_data)
        raise web.seeother('/%s/list' % model.name)

class info_edit:
    @admin_login_required
    def GET(self, mname, id):
        entity = get_entity(id)
        cids = [cate.id for cate in entity.categories]
        model = entity.model
        eform = entity_form()
        eform.cids.set_value(cids)
        form = info_form(model.name)
        info = getattr(entity, model.name)
        eform.fill(entity)
        eform.cids.value = cids
        form.fill(info)

        submodels = model.children
        formset = {}
        if submodels:
            for submodel in submodels:
                subinfos = getattr(info, submodel.name+'s')
                forms = []
                for i, subinfo in enumerate(subinfos):
                    subformobj = info_form(submodel.name, str(i))
                    subformobj.fill(subinfo, '%s-%s' % (submodel.name, str(i)))
                    subformobj.id = subinfo.id
                    forms.append(subformobj)
                forms.append(info_form(submodel.name, '__prefix__'))
                subform = dict(prefix=submodel.name, title=submodel.title, forms=forms)
                formset.update({submodel.name: subform})

        # populate multi value field
        pd = []
        for item in form.inputs:
            if isinstance(item, MyCheckboxGroup):
                pd.append(item.name)
        for k in pd:
            getattr(form, k).set_value(eval(getattr(info, k)))

        categories = category_tree()
        data = web.input()
        req = web.ctx.req
        req.update({
            'eform': eform,
            'form': form,
            'formset': formset,
            'mname': model.name,
            'mtitle': model.title,
            'categories': categories,
        })
        return admin_render.info_edit(**req)

    @admin_login_required
    def POST(self, mname, id):
        entity = get_entity(id)
        model = entity.model
        eform = entity_form()
        form = info_form(model.name)
        data = web.input(cids=[])
        bv = eform.validates()
        v = form.validates()
        is_unique_slug = not get_other_entities(int(id), eform.slug.get_value())

        #if web.config.dev_debug:
        #    import pdb
        #    pdb.set_trace()

        submodels = model.children
        sfvs = []
        formset = {}
        if submodels:
            for submodel in submodels:
                forms_total = int(getattr(data, submodel.name+'-TOTAL_FORMS'))
                forms = []
                for i in range(forms_total):
                    subformobj = info_form(submodel.name, str(i))
                    sfv = subformobj.validates()
                    sfvs.append(sfv)
                    idkey = '%s-%d-%s' % (submodel.name, i, 'id')
                    subformobj.id = int(getattr(data, idkey)) if hasattr(data, idkey) else None
                    subformobj.will_delete = hasattr(data, '%s-%d-%s' % (submodel.name, i, 'DELETE'))
                    forms.append(subformobj)
                forms.append(info_form(submodel.name, '__prefix__'))
                subform = dict(prefix=submodel.name, title=submodel.title, forms=forms)
                formset.update({submodel.name: subform})

        sfsv = reduce(bool.__and__, sfvs) if sfvs else True

        if not bv or not v or not sfsv or not is_unique_slug:
            if not is_unique_slug:
                eform.slug.note = u"%s已存在，请重新指定。" % (eform.slug.get_value())
            categories = category_tree()
            eform.cids.set_value(data.cids)
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
                'eform': eform,
                'form': form,
                'formset': formset,
                'mname': model.name,
                'mtitle': model.title,
                'categories': categories,
            })
            return admin_render.info_edit(**req)
        eform_data = eform.d
        eform_data.cids = data.cids
        eform_data.updated_time = datetime.now()
        form_data = form.d
        sforms_data = {}
        if formset:
            for sform_name, subform in formset.items():
                formsnum = len(subform['forms'])
                for i, subformobj in enumerate(subform['forms']):
                    if i < formsnum-1:
                        sfdata = subformobj.d
                        sfdata.id = subformobj.id
                        sfdata.will_delete = subformobj.will_delete
                        sforms_data.setdefault(sform_name, []).append(sfdata)

        # populate multi value field
        pd = {}
        for item in form.inputs:
            if isinstance(item, MyCheckboxGroup):
                pd[item.name] = []
        pdata = web.input(**pd)
        for k in pd.keys():
            setattr(form_data, k, str(getattr(pdata, k)))

        save_info(model, int(id), eform_data, form_data, sforms_data)
        raise web.seeother('/%s/list' % model.name)

class info_delete:
    @admin_login_required
    def GET(self, mname, id):
        #del_entity(id)
        entity = get_entity(id)
        model = entity.model
        info = getattr(entity, model.name)
        submodels = model.children
        if submodels:
            for submodel in submodels:
                subinfos = getattr(info, submodel.name+'s')
                if subinfos:
                    for subinfo in subinfos:
                        web.ctx.orm.delete(subinfo)

        if info is not None:
            web.ctx.orm.delete(info)
        if entity is not None:
            web.ctx.orm.delete(entity)

        web.ctx.orm.commit()
        raise web.seeother('/%s/list' % model.name)

#-------------------------------
# util views
#-------------------------------
class create_table:
    @admin_login_required
    def GET(self, id):
        model = get_model(id)
        create_schema(model)
        activate_model(model)
        raise web.seeother('/model/index')

class drop_table:
    @admin_login_required
    def GET(self, id):
        model = get_model(id)
        infonum = count_infos(model)
        if infonum > 0 and not web.input(yes=None).yes:
            req = web.ctx.req
            req.update({
                'model': model,
                'infonum': infonum,
            })
            return admin_render.drop_schema_confirm(**req)

        drop_schema(model)
        inactivate_model(model)
        raise web.seeother('/model/index')


urls = (
        '/model/index', model_index,
        '/model/add', model_add,
        '/model/(\d+)/edit', model_edit,
        '/model/(\d+)/view', model_view,
        '/model/(\d+)/delete', model_delete,
        '/model/(\d+)/create_table', create_table,
        '/model/(\d+)/drop_table', drop_table,

        '/field/index', field_index,
        '/field/add', field_add,
        '/field/(\d+)/edit', field_edit,
        '/field/(\d+)/view', field_view,
        '/field/(\d+)/delete', field_delete,

        '/relation/index', relation_index,
        '/relation/add', relation_add,
        '/relation/(\d+)/edit', relation_edit,
        '/relation/(\d+)/delete', relation_delete,

        '/info/admin', info_admin,
        '/info/index', info_index,
        '/(.+)/list', info_list,
        '/(.+)/add', info_add,
        '/(.+)/(\d+)/edit', info_edit,
        '/(.+)/(\d+)/delete', info_delete,
)
