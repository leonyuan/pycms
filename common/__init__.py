import web
from common.config import *
from common.util import render_mako
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from common.config import template_dir


dburl = '%s://%s:%s@%s/%s?charset=utf8' % (db_engine, db_user, db_password, db_host, db_name)
engine = create_engine(dburl, pool_size=100, pool_recycle=7200, echo=debug) #echo: if True print all sql statement, else False.
Base = declarative_base()
DBSession = sessionmaker(bind=engine)

def load_sqla(handler):
    web.ctx.orm = scoped_session(DBSession)
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()

render = render_mako(
            directories=[template_dir],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )


