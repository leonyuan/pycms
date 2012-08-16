#encoding=utf-8
from web import form


vnotnull = form.Validator(u"请输入${description}", bool)
vpass = form.regexp(r".{3,20}$", u'密码长度为3到20个字符')
vemail = form.regexp(r".*@.*", u"要求有效的email地址")
vsamepass = form.Validator(u"两次输入的密码必须相同", lambda i: i.password == i.password2)
