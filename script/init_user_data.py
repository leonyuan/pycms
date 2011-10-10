#encoding=utf-8
from account.model import User
from common import DBSession


def init():
    session = DBSession()

    admin = User('admin', 'admin@xxxx.com')
    admin.set_password('asdfjk')
    admin.is_active=True
    admin.is_superuser=True

    ahao = User('ahao', 'ahao@163.com')
    ahao.set_password('asdfjk')

    session.add(admin)
    session.add(ahao)
    session.commit()

if __name__ == '__main__':
    init()
