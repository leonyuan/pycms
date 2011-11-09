#encoding=utf-8
import web
from common.form import *
from common.widget import MyTextbox, MyPassword, MyRadio, MyButton, MyDropdown, MyLongText


login_form = web.form.Form(
    web.form.Textbox('username', web.form.notnull,
        size=20,
        description=u"用户名:"),
    web.form.Password('password', web.form.notnull,
        size=20,
        description=u"密码:"),
    web.form.Button('login', html=u'登录'),
)


