import os
import sys
from os.path import abspath, dirname

sys.path.insert(0, abspath(dirname(__file__)))

from app import app
application = app.wsgifunc()
