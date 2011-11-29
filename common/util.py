#encoding=utf-8
import web
from web.contrib.template import render_mako as _render_mako
from sqlalchemy import func
from common.config import default_page_size


def login_required(view_func):
    from account.auth import is_logined
    def __dec_func(viewobj, *args, **kwargs):
        if is_logined():
            return view_func(viewobj, *args, **kwargs)
        else:
            if web.ctx.method == 'GET':
                redirect_url = web.ctx.homepath + web.ctx.fullpath
                raise web.seeother('/login?redirect_to=' + redirect_url, True)
            else:
                raise web.seeother('/login', True)
    return __dec_func


ERROR_KEY = '_err'
VALIDATE_ERROR_KEY = '_verr'

class Context:
    def __init__(self, dict=None):
        self.data = {}
        if dict is not None:
            self.data.update(dict)

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        raise KeyError(key)

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, key):
        return key in self.data

    def has_key(self, key):
        return key in self.data

    def update(self, dict=None):
        if dict is None:
            return
        self.data.update(dict)

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def iterkeys(self):
        return self.data.iterkeys()

    def iteritems(self):
        return self.data.iteritems()

    def itervalues(self):
        return self.data.itervalues()

    def _doerr(self, k, m):
        if not k in self.data:
            self.data[k] = []
        self.data[k].append(m)

    def err(self, msg):
        self._doerr(ERROR_KEY, msg)

    def verr(self, fld, msg):
        if not VALIDATE_ERROR_KEY in self.data:
            self.data[VALIDATE_ERROR_KEY] = {}
        self.data[VALIDATE_ERROR_KEY][fld] = msg

    def add_form_err(form):
        if form.note:
            self.err(form.note)
        for fld in form.inputs:
            if fld.note:
                self.verr(fld.name, fld.note)


context = Context

class render_mako(_render_mako):
    def render(self, filename, **kwargs):
        t = self._lookup.get_template(filename)
        return t.render(**kwargs)

def yesorno(b):
    return b and u"是" or u"否"

def paging(pno, pnum):
    pl = []
    pl.extend(range(1, (pnum > 2 and 2 or pnum)+1))
    pl.extend(range(pnum-1, pnum+1))
    pl.extend(range(pno-2, pno+3))
    for i in range(len(pl)-1,-1,-1):
        if pl[i] < 1 or pl[i] > pnum:
            del pl[i]

    uniqs = set()
    pl2 = []
    for p in pl:
        if p in uniqs:
            continue
        uniqs.add(p)
        pl2.append(p)

    pl2.sort()

    if len(pl2) > 4:
        if pl2[2] > pl2[1]+1:
            pl2.insert(2, 0)
        if pl2[-3]+1 < pl2[-2]:
            pl2.insert(-2, 0)

    return pl2

class Pagination(object):
    def __init__(self, cls, pno=1, psize=default_page_size):
        self.cls = cls
        self.pno = int(pno)
        self.psize = psize
        self.recnum = 0
        self.pnum = 0
        self._queryset = None
        self._paginations = None

    @property
    def queryset(self):
        if self._queryset is None:
            offset = (self.pno-1) * self.psize
            self.recnum = web.ctx.orm.query(func.count(self.cls.id)).scalar()
            self.pnum = self.recnum / self.psize + (self.recnum % self.psize > 0 and 1 or 0)
            self._queryset = web.ctx.orm.query(self.cls).order_by(self.cls.id.desc()).offset(offset).limit(self.psize)
        return self._queryset

    @property
    def paginations(self):
        if self._paginations is None:
            self._pagination = paging(self.pno, self.pnum)
        return self._pagination


