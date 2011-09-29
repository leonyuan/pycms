from common import DBSession
from models.model import Model
from models.util import build_model, create_table, drop_table
from models.dbutil import get_model


def create():
    session = DBSession()

    model = session.query(Model).get(1)
    model_cls = build_model(model)
    create_table(model_cls)

def drop():
    session = DBSession()

    model = session.query(Model).get(1)
    model_cls = build_model(model)
    drop_table(model_cls)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        create()
    elif sys.argv[1] == 'drop':
        drop()


