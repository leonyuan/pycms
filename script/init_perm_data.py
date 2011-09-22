#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from account.model import User, Permission
from common import Session


def main():
    session = Session()

    p1=Permission(u'内容', 'content')
    p2=Permission(u'用户', 'user')

    p11=Permission(u'内容管理', 'content_admin')
    p11.parent=p1
    p111=Permission(u'文章管理', 'article_admin')
    p111.parent=p11
    p112=Permission(u'栏目管理', 'category_index')
    p112.parent=p11
    p113=Permission(u'模板管理', 'template_index')
    p113.parent=p11

    p21=Permission(u'用户管理', 'user_admin')
    p21.parent=p2
    p211=Permission(u'用户维护', 'user_index')
    p211.parent=p21
    p212=Permission(u'用户组维护', 'group_index')
    p212.parent=p21

    session.add(p1)
    session.add(p2)
    session.add(p11)
    session.add(p111)
    session.add(p112)
    session.add(p113)
    session.add(p21)
    session.add(p211)
    session.add(p212)
    session.commit()

if __name__ == '__main__':
    main()
