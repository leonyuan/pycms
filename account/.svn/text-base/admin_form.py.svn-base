#encoding=utf-8
import web
from pycms.form.widget import *
from pycms.form.validator import *


editpwd_form = web.form.Form(
    MyPassword('password', vnotnull, vpass, required=True, size=20, description=u"新密码"),
    MyPassword('password2', vnotnull, vpass, required=True, size=20, description=u"确认密码"),
    validators=[vsamepass],
)

user_form = web.form.Form(
    MyTextbox('username', vnotnull, required=True, size=20, description=u"用户名"),
    MyTextbox('email', vnotnull, vemail, required=True, size=20, description=u"电子邮件"),
    MyCheckbox('is_active', value='1', description=u"是否激活"),
    MyCheckbox('is_superuser', value='1', description=u"是否超级用户"),
)

group_form = web.form.Form(
    MyTextbox('name', vnotnull, required=True, size=20, description=u"组名"),
)

