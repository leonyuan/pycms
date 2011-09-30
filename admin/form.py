#encoding=utf-8
import web
from web import form
from admin.util import render
from admin.widget import MyTextbox, MyPassword


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
    MyTextbox('username', vnotnull, size=20, description=u"用户名"),
    MyPassword('password', vnotnull, size=20, description=u"密码"),
    web.form.Button('login', html=u'登录'),
)

model_form = web.form.Form(
    MyTextbox('title', vnotnull, size=20, description=u"模型名称"),
    MyTextbox('name', vnotnull, size=20, description=u"模型代码"),
    web.form.Button('submit', html=u'提交'),
)

field_form = web.form.Form(
    MyTextbox('type', vnotnull, size=20, description=u"属性类型"),
    MyTextbox('title', size=20, description=u"属性名称"),
    MyTextbox('name', vnotnull, size=20, description=u"属性代码"),
    MyTextbox('length', size=20, description=u"数据长度"),
    web.form.Button('submit', html=u'提交'),
)

relation_form = web.form.Form(
    MyTextbox('type', vnotnull, size=20, description=u"关联类型"),
    MyTextbox('title', size=20, description=u"关联名称"),
    MyTextbox('name', vnotnull, size=20, description=u"关联代码"),
    MyTextbox('target', vnotnull, size=20, description=u"目的模型"),
    MyTextbox('backref', size=20, description=u"反向引用"),
    web.form.Button('submit', html=u'提交'),
)

template_form = web.form.Form(
    MyTextbox('name', vnotnull, size=20, description=u"模板名称"),
    MyTextbox('file', vnotnull, size=20, description=u"模板文件"),
    web.form.Button('submit', html=u'提交'),
)

category_form = web.form.Form(
    MyTextbox('parent_id', size=20, description=u"上级栏目"),
    MyTextbox('name', vnotnull, size=20, description=u"栏目名称"),
    MyTextbox('slug', vnotnull, size=20, description=u"英文缩写"),
    MyTextbox('model_id', vnotnull, size=20, description=u"默认模型"),
    web.form.Button('submit', html=u'提交'),
)

article_form = web.form.Form(
    MyTextbox('cid', vnotnull, size=20, description=u"栏目"),
    MyTextbox('title', vnotnull, size=20, description=u"标题"),
    MyTextbox('keywords', size=20, description=u"关键词"),
    MyTextbox('summary', size=20, description=u"摘要"),
    MyTextbox('content', vnotnull, size=20, description=u"内容"),
    web.form.Button('submit', html=u'提交'),
)

