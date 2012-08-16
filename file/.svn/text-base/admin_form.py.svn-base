#encoding=utf-8
import web

from pycms.form.widget import *
from pycms.form.validator import *

file_form = web.form.Form(
    MyTextbox('filename', vnotnull, required=True, size=20, description=u"文件名称"),
    MyLongText('content', description=u"内容"),
)

