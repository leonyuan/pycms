#encoding=utf-8
import web
from web import form
from admin.util import render
from admin.widget import MyTextbox, MyPassword, MyRadio, MyButton, MyDropdown, MyLongText
from models.dbutil import get_model_by_name


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

vnotnull = form.Validator(u"请输入${description}", bool)
vpass = form.regexp(r".{3,20}$", u'密码长度为3到20个字符')
vemail = form.regexp(r".*@.*", u"要求有效的email地址")
vsamepass = form.Validator(u"两次输入的密码必须相同", lambda i: i.password == i.password2)

admin_login_form = web.form.Form(
    MyTextbox('username', vnotnull, required=True, size=20, description=u"用户名"),
    MyPassword('password', vnotnull, required=True, size=20, description=u"密码"),
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
    MyTextbox('model_id', vnotnull, required=True, size=20, description=u"默认模型"),
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
            web.debug('====fld.type:%s' % fld.type)
            if fld.required:
                form_items.append(WIDGET_TYPE[fld.type](fld.name, vnotnull, required=True, description=fld.title))
            else:
                form_items.append(WIDGET_TYPE[fld.type](fld.name, description=fld.title))

        form = web.form.Form(*form_items)
        _entity_forms_cache[mname] = form
        return form

def entity_form(mname, refresh=False):
    form = _entity_form(mname, refresh)
    return form()

def remove_form_from_cache(mname):
    pass


