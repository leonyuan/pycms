import web
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'mysql')
def mysql_utcnow(element, compiler, **kw):
    return "current_timestamp"


