# debug option
debug = True

# database settings
db_engine = 'mysql'
db_name = 'pycms'
db_user = 'dev'
db_password = '1234'
db_host = 'localhost'

# session settings
session_tablename = 'session'

try:
    from local_config import *
except ImportError:
    pass
