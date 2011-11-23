#encoding=utf-8
from copy import deepcopy
import web
from web import form
from admin.util import render
from models.dbutil import get_model_by_name
from common.widget import *
from common.form import *


class TemplateForm(web.form.Form):

    def __init__(self, *inputs, **kw):
        super(TemplateForm, self).__init__(*inputs, **kw)
        self.template_name = kw.pop('template_name', '')

    def __call__(self, render, x=None):
        o = super(TemplateForm, self).__call__(x)
        o._render = render
        return o

    def render(self):
        return self._render(d=self.d)


admin_login_form = web.form.Form(
    MyTextbox('username', vnotnull, required=True, size=20, description=u"用户名"),
    MyPassword('password', vnotnull, required=True, size=20, description=u"密码"),
)

editpwd_form = web.form.Form(
    MyPassword('password', vnotnull, required=True, size=20, description=u"新密码"),
    MyPassword('password2', vnotnull, required=True, size=20, description=u"确认密码"),
)

user_form = web.form.Form(
    MyTextbox('username', vnotnull, required=True, size=20, description=u"用户名"),
    MyTextbox('email', vnotnull, required=True, size=20, description=u"电子邮件"),
    MyCheckbox('is_active', value='1', description=u"是否激活"),
    #MyRadio('is_superuser', ((1, u'是'), (0, u'否')), size=20, description=u"是否超级用户"),
    MyCheckbox('is_superuser', value='1', description=u"是否超级用户"),
)

group_form = web.form.Form(
    MyTextbox('name', vnotnull, required=True, size=20, description=u"组名"),
)

model_form = web.form.Form(
    MyTextbox('title', vnotnull, required=True, size=20, description=u"模型名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"模型代码"),
    MyTextbox('template_id', vnotnull, required=True, size=20, description=u"模板"),
)

FIELD_TYPE = (
    ('string', u'短文本'),
    ('text', u'长文本'),
    ('integer', u'整数'),
    ('float', u'实数'),
    ('boolean', u'布尔'),
    ('select', u'选择框'),
    ('radio', u'单选钮'),
    ('date', u'日期'),
    ('datetime', u'日期和时间'),
)

field_form = web.form.Form(
    MyDropdown('type', FIELD_TYPE, vnotnull, required=True, description=u"属性类型"),
    MyTextbox('title', size=20, description=u"属性名称"),
    MyTextbox('name', vnotnull, required=True, size=20, class_='input-text', description=u"属性代码"),
    MyTextbox('length', size=20, description=u"数据长度"),
    MyRadio('required', ((1, u'是'), (0, u'否')), size=20, description=u"是否必需"),
)

relation_form = web.form.Form(
    MyTextbox('type', vnotnull, required=True, size=20, description=u"关联类型"),
    MyTextbox('title', size=20, description=u"关联名称"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"关联代码"),
    MyTextbox('target', vnotnull, required=True, size=20, description=u"目的模型"),
    MyTextbox('backref', size=20, description=u"反向引用"),
)

template_form = web.form.Form(
    MyTextbox('name', vnotnull, required=True, size=20, description=u"模板名称"),
    MyTextbox('index_file', vnotnull, required=True, size=20, description=u"频道页"),
    MyTextbox('list_file', vnotnull, required=True, size=20, description=u"列表页"),
    MyTextbox('display_file', vnotnull, required=True, size=20, description=u"内容页"),
)

category_form = web.form.Form(
    MyTextbox('parent_id', size=20, description=u"上级栏目"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"栏目名称"),
    MyTextbox('slug', vnotnull, required=True, size=20, description=u"英文缩写"),
)

base_entity_form = web.form.Form(
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
}

_entity_forms_cache = {}

def _entity_form(mname, refresh=False):
    if mname in _entity_forms_cache and not refresh:
        return _entity_forms_cache[mname]
    else:
        remove_form_from_cache(mname)
        model = get_model_by_name(mname)
        form_items = []
        for fld in model.fields:
            if fld.required:
                form_items.append(WIDGET_TYPE[fld.type](fld.name, vnotnull, required=True, description=fld.title))
            else:
                form_items.append(WIDGET_TYPE[fld.type](fld.name, description=fld.title))
        for rel in model.relations:
            form_items.append(WIDGET_TYPE['integer']('%s_id' % rel.target, description=rel.title))

        form = web.form.Form(*form_items)
        _entity_forms_cache[mname] = form
        return form

def entity_form(mname, refresh=False):
    form = _entity_form(mname, refresh)
    return form()

def remove_form_from_cache(mname):
    if mname in _entity_forms_cache:
        del _entity_forms_cache[mname]


