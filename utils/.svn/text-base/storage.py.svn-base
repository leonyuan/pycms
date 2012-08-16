
class Context:
    ERROR_KEY = '_err'
    VALIDATE_ERROR_KEY = '_verr'

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

