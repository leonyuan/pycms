#encoding=utf-8
from account.model import Permission
from common import DBSession


def init():
    session = DBSession()

    p1=Permission(u'内容', 'content')
    p2=Permission(u'用户', 'user')

    #p11=Permission(u'内容管理', 'content_admin')
    #p11.parent=p1
    p111=Permission(u'实体管理', 'entity_index')
    p111.parent=p1
    p112=Permission(u'栏目管理', 'category_index')
    p112.parent=p1
    p113=Permission(u'模型管理', 'model_index')
    p113.parent=p1
    p114=Permission(u'模板管理', 'template_index')
    p114.parent=p1
    p115=Permission(u'发布管理', 'publish_index')
    p115.parent=p1

    #p21=Permission(u'用户管理', 'user_admin')
    #p21.parent=p2
    p211=Permission(u'用户管理', 'user_index')
    p211.parent=p2
    p212=Permission(u'组管理', 'group_index')
    p212.parent=p2

    session.add(p1)
    session.add(p2)
    #session.add(p11)
    session.add(p111)
    session.add(p112)
    session.add(p113)
    session.add(p114)
    session.add(p115)
    #session.add(p21)
    session.add(p211)
    session.add(p212)
    session.commit()

if __name__ == '__main__':
    init()
