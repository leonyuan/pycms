import web
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import DateTime


cfg = web.config
db = web.database(dbn=cfg.db_engine, user=cfg.db_user, pw=cfg.db_password, db=cfg.db_name)
dbstore = web.session.DBStore(db, cfg.session_tablename)

dburl = '%s://%s:%s@%s/%s?charset=utf8' % (cfg.db_engine, cfg.db_user, \
        cfg.db_password, cfg.db_host, cfg.db_name)
#echo: if True print all sql statement, else False.
engine = create_engine(dburl, pool_size=100, pool_recycle=7200, echo=cfg.debug)
Base = declarative_base()
DBSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
    try:
        return handler()
    except web.HTTPError:
        #web.ctx.orm.commit()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        #web.ctx.orm.expunge_all()
        web.ctx.orm.remove()
        #None
        #web.ctx.orm.commit()

class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'mysql')
def mysql_utcnow(element, compiler, **kw):
    return "current_timestamp"

def populate(obj, data, clz, prefix=''):
    for col in clz.__mapper__.columns:
        field_name = '%s-%s' % (prefix, col.name) if prefix else col.name
        if col.name == 'id':
            continue
        if hasattr(data, field_name):
            val = getattr(data, field_name)
            if not val:
                setattr(obj, col.name, None)
            else:
                setattr(obj, col.name, val)

def populate2(obj, data):
    for k, v in data.items():
        if v is not None and hasattr(obj, k):
            setattr(obj, k, v)


