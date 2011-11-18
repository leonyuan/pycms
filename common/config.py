from os.path import abspath, dirname, join


curdir = abspath(dirname(__file__))

# debug option
debug = True

# database settings
db_engine = 'mysql'
db_name = 'pycms'
db_user = 'dev'
db_password = '1234'
db_host = 'localhost'

# template directory
template_dir = join(curdir, '../templates/')

# session settings
session_tablename = 'session'

# default new user's password
default_password = 'pycms'

try:
    from local_config import *
except ImportError:
    pass
