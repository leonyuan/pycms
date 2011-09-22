#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from account.model import User, Permission
from common import Session


def main():
    session = Session()

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
    main()
