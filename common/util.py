import web
from account.auth import is_logined


def login_required(view_func):
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

    def err(self, m):
        self._doerr(ERROR_KEY, m)

    def verr(self, m):
        self._doerr(VALIDATE_ERROR_KEY, m)


context = Context
