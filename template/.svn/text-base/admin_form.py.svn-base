#encoding=utf-8
import web

from pycms.form.widget import *
from pycms.form.validator import *

template_form = web.form.Form(
    MyTextbox('name', vnotnull, required=True, size=20, description=u"模板名称"),
    MyTextbox('index_file', vnotnull, required=True, size=20, description=u"频道页"),
    MyTextbox('list_file', vnotnull, required=True, size=20, description=u"列表页"),
    MyTextbox('display_file', vnotnull, required=True, size=20, description=u"内容页"),
)

