#encoding=utf-8
from copy import deepcopy
import web
from pycms.model.db import get_model_by_name
from pycms.form.widget import *
from pycms.form.validator import *


model_form = web.form.Form(
    MyTextbox('title', vnotnull, required=True, size=20, description=u"模型名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"模型代码"),
    MyTextbox('template_id', size=20, description=u"模板"),
    MyTextbox('parent_id', size=20, description=u"父模型"),
    MyTextarea('description', description=u"描述"),
)

FIELD_TYPE = {
        'string': u'短文本',
        'text': u'长文本',
        'integer': u'整数',
        'float': u'实数',
        'boolean': u'布尔',
        'select': u'列表框',
        'radio': u'单选钮',
        'checkbox': u'复选钮',
        'date': u'日期',
        'time': u'时间',
        }


field_string_form = web.form.Form(
    MyTextbox('title', vnotnull, required=True, size=20, description=u"属性名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"属性代码"),
    MyTextbox('length', size=20, description=u"文本长度"),
    MyRadio('required', ((1, u'是'), (0, u'否')), vnotnull, required=True, size=20, description=u"是否必需"),
)

field_text_form = web.form.Form(
    MyTextbox('title', vnotnull, required=True, size=20, description=u"属性名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"属性代码"),
    MyRadio('required', ((1, u'是'), (0, u'否')), size=20, description=u"是否必需"),
    MyTextbox('lines', size=20, description=u"行数"),
    MyRadio('editor', (('simple', u'简单编辑器'), ('feature', u'全功能编辑器')), size=20, description=u"所用编辑器"),
)

field_select_form = web.form.Form(
    MyTextbox('title', vnotnull, required=True, size=20, description=u"属性名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"属性代码"),
    MyTextbox('length', vnotnull, required=True, size=20, description=u"文本长度"),
    MyRadio('required', ((1, u'是'), (0, u'否')), size=20, description=u"是否必需"),
    MyCheckbox('is_multisel', value='1', description=u"允许多选"),
    MyTextbox('options', vnotnull, required=True, size=20, description=u"选项"),
)

field_radio_form = web.form.Form(
    MyTextbox('title', vnotnull, required=True, size=20, description=u"属性名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"属性代码"),
    MyTextbox('length', vnotnull, required=True, size=20, description=u"文本长度"),
    MyRadio('required', ((1, u'是'), (0, u'否')), size=20, description=u"是否必需"),
    MyTextbox('options', vnotnull, required=True, size=20, description=u"选项"),
)

field_checkbox_form = web.form.Form(
    MyTextbox('title', vnotnull, required=True, size=20, description=u"属性名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"属性代码"),
    MyTextbox('length', vnotnull, required=True, size=20, description=u"文本长度"),
    MyRadio('required', ((1, u'是'), (0, u'否')), size=20, description=u"是否必需"),
    MyTextbox('options', vnotnull, required=True, size=20, description=u"选项"),
)

FIELD_FORM_TYPE = {
        'string_form': field_string_form,
        'text_form': field_text_form,
        'select_form': field_select_form,
        'radio_form': field_radio_form,
        'checkbox_form': field_checkbox_form,
}

relation_form = web.form.Form(
    MyTextbox('type', vnotnull, required=True, size=20, description=u"关联类型"),
    MyTextbox('title', size=20, description=u"关联名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"关联代码"),
    MyTextbox('target', vnotnull, required=True, size=20, description=u"目的模型"),
    MyTextbox('backref', size=20, description=u"反向引用"),
)

entity_form = web.form.Form(
    MyTextbox('cids', vnotnull, required=True, size=40, description=u"栏目"),
    MyTextbox('title', vnotnull, required=True, size=40, description=u"标题"),
    MyTextbox('slug', size=20, description=u"英文缩写"),
)

WIDGET_TYPE = {
    'string': MyTextbox,
    'integer': MyTextbox,
    'text': MyLongText,
    'float': MyTextbox,
    'boolean': MyRadio,
    'select': MyDropdown,
    'radio': MyRadio,
    'checkbox': MyCheckboxGroup,
}

_info_forms_cache = {}

def _info_form(mname, prefix='', refresh=False):
    key = '%s-%s' % (mname, prefix) if prefix else mname
    if key in _info_forms_cache and not refresh:
        return _info_forms_cache[key]
    else:
        remove_form_from_cache(key)
        model = get_model_by_name(mname)
        form_items = []
        for fld in model.fields:
            if fld.type == 'select' or fld.type == 'radio' or fld.type == 'checkbox':
                prop_dict = eval(fld.props)
                item = WIDGET_TYPE[fld.type]('%s-%s-%s' % (mname, prefix, fld.name) if prefix else fld.name \
                        , prop_dict['options'], description=fld.title)
            else:
                item = WIDGET_TYPE[fld.type]('%s-%s-%s' % (mname, prefix, fld.name) if prefix else fld.name \
                        , description=fld.title)

            if fld.required:
                item.required = True
                item.validators = (vnotnull,)

            form_items.append(item)

        #for rel in model.relations:
        #    form_items.append(WIDGET_TYPE['integer']('%s_id' % rel.target, description=rel.title))

        form = MyForm(*form_items)
        _info_forms_cache[key] = form
        return form

def info_form(mname, prefix='', refresh=False):
    form = _info_form(mname, prefix, refresh)
    return form()

def remove_form_from_cache(mname):
    if mname in _info_forms_cache:
        del _info_forms_cache[mname]

def typetext(type):
    return FIELD_TYPE[type]
