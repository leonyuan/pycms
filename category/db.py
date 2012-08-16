#encoding=utf-8
import web
from sqlalchemy import func

from pycms.category.model import *
from pycms.model.model import category_entity_asso_table
from pycms.db.util import populate


#-------------------------------
# category persistent method
#-------------------------------
def get_categories():
    return web.ctx.orm.query(Category).all()

def get_haschild_categories():
    cats = web.ctx.orm.query(Category).all()
    retcats = []
    for cat in cats:
        if count_category_children(cat.id) > 0:
            retcats.append(cat)
    return retcats

def get_category(id):
    return web.ctx.orm.query(Category).get(id)

def get_category_by_slug(slug):
    return web.ctx.orm.query(Category).filter_by(slug=slug).first()

def get_other_categories(id, slug):
    return web.ctx.orm.query(Category).filter(Category.slug==slug).filter(Category.id!=id).all()

def get_latest_childcats(cid, count):
    cats = web.ctx.orm.query(Category).filter(Category.parent_id==cid).order_by(Category.id.desc()).all()
    return cats[:count]

def save_category(id, data):
    if id == -1:
        category = Category()
    else:
        category = get_category(id)

    populate(category, data, Category)

    if id == -1:
        web.ctx.orm.add(category)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def new_category(data):
    save_category(-1, data)

def del_category(id):
    category = get_category(id)
    web.ctx.orm.delete(category)
    web.ctx.orm.commit()

def count_category_children(id):
    return web.ctx.orm.query(func.count(Category.id)).filter_by(parent_id=id).scalar()

def count_category():
    return web.ctx.orm.query(func.count(Category.id)).scalar()

def build_tree(pid, level, prefix, getsubcat_func):
    cates = getsubcat_func(pid)
    ret_cates = []
    cnt = len(cates)
    super_prefix = prefix
    the_prefix = ''
    for i, cate in enumerate(cates):
        cate.level = level
        if level > 0:
            if i == cnt-1:
                the_prefix = '&nbsp;'*2+u'└─'
                child_prefix = super_prefix + '&nbsp;'*6
            else:
                the_prefix = '&nbsp;'*2+u'├─'
                child_prefix = super_prefix + '&nbsp;'*2+u'│&nbsp;'
        else:
            the_prefix = ''
            child_prefix = '&nbsp;'*2

        cate.prefix = super_prefix + the_prefix
        ret_cates.append(cate)
        ret_cates.extend(build_tree(cate.id, level+1, child_prefix, getsubcat_func))

    return ret_cates


def category_tree(pid=None, level=0, prefix=''):
    cats = web.ctx.orm.query(Category).order_by(Category.id).all()

    def get_subcat(pid):
        results = []
        for cat in cats:
            if cat.parent_id == pid:
                results.append(cat)

        return results

    return build_tree(pid, level, prefix, get_subcat)

def category_tree2(pid=None):
    cates = web.ctx.orm.query(Category).filter_by(parent_id=pid).all()
    html = ''
    for i, cate in enumerate(cates):
        html += '<li><a href="%s/index?cid=%s" target="right">%s</a>' % (cate.model.name, cate.id, cate.name)

        if count_category_children(cate.id) > 0:
            html += '<ul>'
            html += category_tree2(cate.id)
            html += '</ul>'
        html += '</li>'

    return html

def category_tree3(pid=None, level=0, prefix=''):
    stmt = web.ctx.orm.query('category_id', func.count('*').label('entnum')) \
            .select_from(category_entity_asso_table).group_by('category_id').subquery()
    catns = web.ctx.orm.query(Category, stmt.c.entnum, Template.name) \
            .outerjoin(stmt, Category.id==stmt.c.category_id) \
            .outerjoin(Template).order_by(Category.id).all()

    def get_subcat(pid):
        results = []
        for cat, n, tname in catns:
            if cat.parent_id == pid:
                cat.entnum = n or 0
                cat.tname = tname
                results.append(cat)

        return results

    return build_tree(pid, level, prefix, get_subcat)

def get_category_ancestors(category):
    ancestors = []
    if category.parent is not None:
        ancestors.extend(get_category_ancestors(category.parent))
    ancestors.append((category.id, category.name, category.slug))
    return ancestors



