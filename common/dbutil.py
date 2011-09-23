import web
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'mysql')
def mysql_utcnow(element, compiler, **kw):
    return "current_timestamp"

def populate(obj, data, clz):
    for col in clz.__mapper__.columns:
        if col.name == 'id':
            continue
        if hasattr(data, col.name) and getattr(data, col.name):
            setattr(obj, col.name, getattr(data, col.name))

def populate2(obj, data):
    for k, v in data.items():
        if v is not None and hasattr(obj, k):
            setattr(obj, k, v)


