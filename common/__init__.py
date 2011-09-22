from os.path import abspath, dirname, join
import web
from common.config import *
from web.contrib.template import render_mako
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


dburl = '%s://%s:%s@%s/%s?charset=utf8' % (db_engine, db_user, db_password, db_host, db_name)
engine = create_engine(dburl, echo=debug) #echo: if True print all sql statement, else False.
Base = declarative_base()
Session = sessionmaker(bind=engine)

def load_sqla(handler):
    web.ctx.orm = scoped_session(Session)
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

curdir = abspath(dirname(__file__))
render = render_mako(
            directories=[join(curdir, '../templates/')],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )

