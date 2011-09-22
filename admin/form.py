#encoding=utf-8
import web
from admin.util import render


class TemplateForm(web.form.Form):

    def __init__(self, *inputs, **kw):
        super(TemplateForm, self).__init__(*inputs, **kw)
        self.template_name = kw.pop('template_name', '')

    def __call__(self, render, x=None):
        o = super(TemplateForm, self).__call__(x)
        o._render = render
        return o

    def render(self):
        print '====start render form %s, %s ' % (self.template_name, self.d)
        return self._render(d=self.d)

admin_login_form = web.form.Form(
    web.form.Textbox('username', web.form.notnull, size=20, description=u"用户名:"),
    web.form.Password('password', web.form.notnull, size=20, description=u"密码:"),
    web.form.Button('login', html=u'登录'),
)

template_form = web.form.Form(  #TemplateForm(
    web.form.Textbox('name', web.form.notnull, size=20, description=u"模板名称:"),
    web.form.Textbox('file', web.form.notnull, size=20, description=u"模板文件:"),
    web.form.Button('submit', html=u'提交'),
    template_name='template_form',
)

category_form = web.form.Form(
    web.form.Textbox('parent_id', size=20, description=u"上级栏目:"),
    web.form.Textbox('name', web.form.notnull, size=20, description=u"栏目名称:"),
    web.form.Textbox('slug', web.form.notnull, size=20, description=u"英文缩写:"),
    web.form.Textbox('template_id', web.form.notnull, size=20, description=u"所用模板:"),
    web.form.Button('submit', html=u'提交'),
)

