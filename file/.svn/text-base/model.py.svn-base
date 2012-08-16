#encoding=utf-8
'''
Template model defination.
'''

import os
import web
from sqlalchemy import Table, Column, Integer, String

from pycms.db.util import Base, utcnow


class File(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = filepath[filepath.rfind(os.path.sep)+1:]

    @property
    def content(self):
        f = open(self.filepath, 'r')
        lines = f.readlines()
        f.close()
        print 'content==>[%s]' % lines
        return lines

    def __repr__(self):
        return "<File('%s')>" % (self.filepath)

