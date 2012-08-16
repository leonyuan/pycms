#encoding=utf-8
import web

from pycms.form.widget import *
from pycms.form.validator import *
from pycms.category.db import get_category_by_slug, get_other_categories


def catslug_unique(data):
    if data.id < 1:
        return get_category_by_slug(data.slug) is None
    else:
        return not get_other_categories(data.id, data.slug)

vunique_slug = web.form.Validator(u"英文缩写已存在，请重新指定。", catslug_unique)

category_form = web.form.Form(
    #web.form.Hidden('id', size=10, description=u"ID"),
    MyTextbox('parent_id', size=20, description=u"上级栏目"),
    MyTextbox('name', vnotnull, required=True, size=20, description=u"栏目名称"),
    MyTextbox('slug', vnotnull, required=True, size=20, description=u"英文缩写"),
    MyTextbox('template_id', size=20, description=u"模板"),
    #validators=[vunique_slug],
)

