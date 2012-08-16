#encoding=utf-8
import web
from sqlalchemy import func
from sqlalchemy.orm import aliased

from pycms.model.model import *
from pycms.model.util import build_model
from pycms.db.util import populate
from pycms.category.model import Category
from pycms.category.db import get_category, get_category_ancestors
from pycms.account.model import User


#-------------------------------
# info persistent method
#-------------------------------
def get_infos(model, cid=None, limit=None):
    model_cls = build_model(model)
    if cid is None:
        return web.ctx.orm.query(model_cls).order_by(model_cls.id.desc()).all()
    else:
        if limit is None:
            return web.ctx.orm.query(model_cls).filter(model_cls.categories.any(id=cid)) \
                    .order_by(model_cls.id.desc()).all()
        else:
            return web.ctx.orm.query(model_cls).filter(model_cls.categories.any(id=cid)) \
                    .order_by(model_cls.id.desc()).limit(limit)

def get_info(model, id):
    model_cls = build_model(model)
    return web.ctx.orm.query(model_cls).get(id)

def count_infos(model):
    model_cls = build_model(model)
    return web.ctx.orm.query(func.count(model_cls .id)).scalar()

def new_info(model, base_data, data, sforms_data):
    save_info(model, -1, base_data, data, sforms_data)

def save_info(model, id, base_data, data, sforms_data):
    model_cls = build_model(model)
    submodels = model.children
    submodel_cls_d = {}
    if submodels:
        for submodel in submodels:
            submodel_cls = build_model(submodel)
            submodel_cls_d[submodel.name] = submodel_cls

    subinfo_d = {}
    if id == -1:
        entity = Entity()
        info = model_cls()
        if submodel_cls_d:
            for smodel_name, submodel_cls in submodel_cls_d.items():
                if smodel_name in sforms_data:
                    subinfo_d[smodel_name] = [submodel_cls() for i in range(len(sforms_data[smodel_name]))]

    else:
        entity = get_entity(id)
        info = getattr(entity, model.name)
        if submodel_cls_d:
            for smodel_name, submodel_cls in submodel_cls_d.items():
                persist_infos = getattr(info, smodel_name+'s')
                if smodel_name in sforms_data:
                    subinfo_d[smodel_name] = persist_infos
                    for i in range(len(sforms_data[smodel_name])-len(persist_infos)):
                        subinfo_d[smodel_name].append(submodel_cls())

    populate(entity, base_data, Entity)
    populate(info, data, model_cls)
    if subinfo_d:
        for smodel_name, subinfos in subinfo_d.items():
            for i, subinfo in enumerate(subinfos):
                sform_data = sforms_data[smodel_name][i] if smodel_name in sforms_data else None
                if sform_data:
                    populate(subinfo, sform_data, submodel_cls_d[smodel_name], '%s-%s' % (smodel_name, str(i)))
                    if subinfo.id is not None:
                        subinfo.will_delete = sform_data.will_delete

    for i in range(len(entity.categories)-1,-1,-1):
        del entity.categories[i]
    for cid in base_data.cids:
        if cid:
            entity.categories.append(get_category(int(cid)))

    if id == -1:
        entity.model = model
        info.entity = entity
        if subinfo_d:
            for smodel_name, subinfos in subinfo_d.items():
                for subinfo in subinfos:
                    getattr(info, smodel_name+'s').append(subinfo)
                    web.ctx.orm.add(subinfo)

        web.ctx.orm.add(entity)
        web.ctx.orm.add(info)
    else:
        if subinfo_d:
            for smodel_name, subinfos in subinfo_d.items():
                for subinfo in subinfos:
                    if subinfo.id is None:
                        getattr(info, smodel_name+'s').append(subinfo)
                        web.ctx.orm.add(subinfo)
                    elif subinfo.will_delete:
                        persist_infos = getattr(info, smodel_name+'s')
                        persist_infos.remove(subinfo)
                        web.ctx.orm.delete(subinfo)

        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_info(model, id):
    info = get_info(model, id)
    web.ctx.orm.delete(info)
    web.ctx.orm.commit()

def get_latest_infos(mname, cid, count):
    model = get_model_by_name(mname)
    return get_infos(model, cid, count)

def query_eids_of_model(model):
    return web.ctx.orm.query(Entity.id).filter(Entity.model_id==model.id).all()

def info_record_query1(model, title, cid):
    search_query = web.ctx.orm.query(Entity, User.username).join(Entity.user) \
            .filter(Entity.model_id==model.id).order_by(Entity.id.desc())
    if title:
        search_query = search_query.filter(Entity.title.like('%%%s%%' % title))
    if cid:
        search_query = search_query.filter(Entity.categories.any(id=cid))
    return search_query

def info_count_query1(model, title, cid):
    search_query = web.ctx.orm.query(Entity.id).filter(Entity.model_id==model.id)
    if title:
        search_query = search_query.filter(Entity.title.like('%%%s%%' % title))
    if cid:
        search_query = search_query.filter(Entity.categories.any(id=cid))
    return search_query

def search_record_query(model, title, cslug):
    search_query = web.ctx.orm.query(Entity).filter(Entity.model_id==model.id).order_by(Entity.id.desc())
    if title:
        search_query = search_query.filter(Entity.title.like('%%%s%%' % title))
    if cslug:
        search_query = search_query.filter(Entity.categories.any(slug=cslug))
    return search_query

def search_count_query(model, title, cslug):
    search_query = web.ctx.orm.query(Entity.id).filter(Entity.model_id==model.id)
    if title:
        search_query = search_query.filter(Entity.title.like('%%%s%%' % title))
    if cslug:
        search_query = search_query.filter(Entity.categories.any(slug=cslug))
    return search_query

def info_record_query2(cid):
    search_query = web.ctx.orm.query(Entity).filter(Entity.categories.any(id=cid)).order_by(Entity.id.desc())
    return search_query

def info_count_query2(cid):
    search_query = web.ctx.orm.query(Entity.id).filter(Entity.categories.any(id=cid)).order_by(Entity.id.desc())
    return search_query


#-------------------------------
# entity persistent method
#-------------------------------
#def get_entities():
#    return web.ctx.orm.query(Entity).all()

def get_entities(cid=None, limit=None):
    if cid is None:
        return web.ctx.orm.query(Entity).order_by(Entity.id.desc()).all()
    else:
        if limit is None:
            return web.ctx.orm.query(Entity).filter(Entity.categories.any(id=cid)) \
                    .order_by(Entity.id.desc()).all()
        else:
            return web.ctx.orm.query(Entity).filter(Entity.categories.any(id=cid)) \
                    .order_by(Entity.id.desc()).limit(limit).all()

def get_entity(id):
    return web.ctx.orm.query(Entity).get(id)

def get_entity_by_slug(slug):
    if not slug:
        return None
    ents = web.ctx.orm.query(Entity).filter_by(slug=slug).all()
    if ents:
        return ents[0]
    return None

def get_other_entities(id, slug):
    if not slug:
        return None
    return web.ctx.orm.query(Entity).filter(Entity.slug==slug).filter(Entity.id!=id).all()

def count_entity():
    return web.ctx.orm.query(func.count(Entity.id)).scalar()

def save_entity(id, data):
    if id == -1:
        entity = Entity()
    else:
        entity = get_entity(id)

    populate(entity, data, Entity)

    if id == -1:
        web.ctx.orm.add(entity)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_entity(id):
    entity = get_entity(id)
    web.ctx.orm.delete(entity)
    web.ctx.orm.commit()

def get_entitys_category_ancestors(entity):
    return get_category_ancestors(entity.categories[0])

def get_latest_entities(cid, count):
    return get_entities(cid, count);

def entity_record_query1():
    return web.ctx.orm.query(Entity, Model.title, User.username).join(Entity.model) \
            .join(Entity.user).order_by(Entity.id.desc())

def entity_count_query1():
    return web.ctx.orm.query(Entity.id)

def catent_cname(eids):
    CatEntAsso = aliased(category_entity_asso_table)
    stmt = web.ctx.orm.query(CatEntAsso).filter(CatEntAsso.c.entity_id.in_(eids)).subquery()
    return web.ctx.orm.query(Category.name, stmt.c.entity_id).join(stmt, Category.id==stmt.c.category_id).all()

def cats_of_ents(eids):
    CatEntAsso = aliased(category_entity_asso_table)
    stmt = web.ctx.orm.query('category_id', func.count('*').label('entnum')).select_from(CatEntAsso) \
            .filter(CatEntAsso.c.entity_id.in_(eids)).group_by('category_id').subquery()
    return web.ctx.orm.query(Category, stmt.c.entnum).join(stmt, Category.id==stmt.c.category_id) \
            .order_by(Category.id).all()

#-------------------------------
# model persistent method
#-------------------------------
def get_models():
    return web.ctx.orm.query(Model).all()

def get_top_models():
    return web.ctx.orm.query(Model).filter_by(is_active=True).filter(Model.parent == None).all()

def get_top_models_with_entnum():
    stmt = web.ctx.orm.query(Entity.model_id, func.count('*').label('entnum')) \
            .group_by(Entity.model_id).subquery()
    models = web.ctx.orm.query(Model, stmt.c.entnum) \
            .outerjoin(stmt, Model.id==stmt.c.model_id) \
            .filter(Model.is_active==True).filter(Model.parent==None) \
            .order_by(Model.id).all()
    return models


def get_active_models():
    return web.ctx.orm.query(Model).filter_by(is_active=True).all()

def get_model_by_name(name):
    return web.ctx.orm.query(Model).filter_by(name=name).first()

def get_other_models(id, name):
    return web.ctx.orm.query(Model).filter(Model.name==name).filter(Model.id!=id).all()

def get_model(id):
    return web.ctx.orm.query(Model).get(id)

def save_model(id, data):
    if id == -1:
        model = Model()
    else:
        model = get_model(id)

    populate(model, data, Model)

    if id == -1:
        web.ctx.orm.add(model)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_model(id):
    model = get_model(id)
    web.ctx.orm.delete(model)
    web.ctx.orm.commit()

def activate_model(model):
    model.is_active = True
    web.ctx.orm.flush()
    web.ctx.orm.commit()

def inactivate_model(model):
    model.is_active = False
    web.ctx.orm.flush()
    web.ctx.orm.commit()


#-------------------------------
# field persistent method
#-------------------------------
def get_fields(mid):
    return web.ctx.orm.query(Field).filter_by(model_id=mid).order_by(Field.id).all()

def get_field(id):
    return web.ctx.orm.query(Field).get(id)

def save_field(id, data):
    if id == -1:
        field = Field()
    else:
        field = get_field(id)

    populate(field, data, Field)
    if hasattr(data, 'type'):
        if data.type == 'text':
            prop_dict = dict(lines=data.lines, editor=data.editor)
            field.props = str(prop_dict)
        elif data.type == 'select' or data.type == 'radio' or data.type == 'checkbox':
            prop_dict = dict(options=data.options)
            if data.type == 'select':
                prop_dict['is_multisel'] = data.is_multisel
            field.props = str(prop_dict)

    if id == -1:
        web.ctx.orm.add(field)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_field(id):
    field = get_field(id)
    web.ctx.orm.delete(field)
    web.ctx.orm.commit()

#-------------------------------
# relation persistent method
#-------------------------------
def get_relations(mid):
    return web.ctx.orm.query(Relation).filter_by(model_id=mid).order_by(Relation.id).all()

def get_relation(id):
    return web.ctx.orm.query(Relation).get(id)

def save_relation(id, data):
    if id == -1:
        relation = Relation()
    else:
        relation = get_relation(id)

    populate(relation, data, Relation)

    if id == -1:
        web.ctx.orm.add(relation)
    else:
        web.ctx.orm.flush()
    web.ctx.orm.commit()

def del_relation(id):
    relation = get_relation(id)
    web.ctx.orm.delete(relation)
    web.ctx.orm.commit()

