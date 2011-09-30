#encoding=utf-8
import web
from sqlalchemy import func
from blog.model import *
from common.dbutil import populate

#-------------------------------
# some utility
#-------------------------------

#-------------------------------
# template persistent method
#-------------------------------
def get_templates():
    return web.ctx.orm.query(Template).all()

def get_template(id):
    return web.ctx.orm.query(Template).get(id)

def save_template(id, data):
    if id == -1:
        template = Template()
    else:
        template = get_template(id)

    populate(template, data, Template)

    if id == -1:
        web.ctx.orm.add(template)
    else:
        web.ctx.orm.flush()

def del_template(id):
    template = get_template(id)
    web.ctx.orm.delete(template)

#-------------------------------
# category persistent method
#-------------------------------
def get_categories():
    return web.ctx.orm.query(Category).all()

def get_category(id):
    return web.ctx.orm.query(Category).get(id)

def new_category(data):
    save_category(-1, data)

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

def del_category(id):
    category = get_category(id)
    web.ctx.orm.delete(category)

def count_category_children(id):
    return web.ctx.orm.query(func.count(Category.id)).filter_by(parent_id=id).scalar()

def category_tree(pid=None, level=0, prefix=''):
    cates = web.ctx.orm.query(Category).filter_by(parent_id=pid).all()
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
        ret_cates.extend(category_tree(cate.id, level+1, child_prefix))

    return ret_cates

def category_tree2(pid=None):
    cates = web.ctx.orm.query(Category).filter_by(parent_id=pid).all()
    html = ''
    for i, cate in enumerate(cates):
        html += '<li><a href="article/index?cid=%s" target="right">%s</a>' % (cate.id, cate.name)

        if count_category_children(cate.id) > 0:
            html += '<ul>'
            html += category_tree2(cate.id)
            html += '</ul>'
        html += '</li>'

    return html

def get_category_ancestors(category):
    ancestors = []
    if category.parent is not None:
        ancestors.extend(get_category_ancestors(category.parent))
    ancestors.append((category.id, category.name))
    return ancestors


#-------------------------------
# article persistent method
#-------------------------------
def new_article(data):
    save_article(-1, data)

def get_article(id):
    return web.ctx.orm.query(Article).get(id)

def get_articles(cid=None, limit=None):
    if cid is None:
        return web.ctx.orm.query(Article).order_by(Article.id.desc()).all()
    else:
        if limit is None:
            return web.ctx.orm.query(Article).filter(Article.categories.any(id=cid)).order_by(Article.id.desc()).all()
        else:
            return web.ctx.orm.query(Article).filter(Article.categories.any(id=cid)).order_by(Article.id.desc()).limit(limit)

def save_article(id, data):
    if id == -1:
        article = Article()
    else:
        article = get_article(id)

    populate(article, data, Article)

    cid = data.cid
    category = get_category(cid)
    article.categories.append(category)

    if id == -1:
        web.ctx.orm.add(article)
    else:
        web.ctx.orm.flush()

def del_article(id):
    article = get_article(id)
    web.ctx.orm.delete(article)

def get_articles_category_ancestors(article):
    return get_category_ancestors(article.categories[0])

def get_latest_articles(cid, count):
    return get_articles(cid, count)


