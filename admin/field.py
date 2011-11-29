#encoding=utf-8
import web
from admin.util import render, admin_login_required
from models.dbutil import get_model, get_fields, save_field, get_field, del_field
from admin.form import field_string_form, field_text_form, FIELD_FORM_TYPE


class index:
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
        return render.field_index(**req)

class add:
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
        return render.field_edit(**req)

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
            return render.field_edit(**req)
        form_data = form.d
        form_data.type = data.type
        form_data.options = data.options
        form_data.model_id = mid
        save_field(-1, form_data)
        raise web.seeother('/model/%s/edit' % mid)

class edit:
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
        return render.field_edit(**req)

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
            return render.field_edit(**req)
        form_data = form.d
        form_data.type = data.type
        form_data.options = data.options
        save_field(int(id), form_data)
        raise web.seeother('/model/%s/edit' % mid)

class delete:
    @admin_login_required
    def GET(self, id):
        del_field(id)
        data = web.input()
        mid = data.mid
        raise web.seeother('/model/%s/edit' % mid)

